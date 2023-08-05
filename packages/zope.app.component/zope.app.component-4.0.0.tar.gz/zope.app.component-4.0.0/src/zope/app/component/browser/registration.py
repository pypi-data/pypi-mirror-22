##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""General registry-related views
"""
import base64
import warnings

from zope import interface, component, schema
from zope.formlib import form
from zope.publisher.browser import BrowserPage
from zope.security.proxy import removeSecurityProxy
import zope.component.interfaces
import zope.publisher.interfaces.browser

import zope.app.pagetemplate
from zope.app.component.i18n import ZopeMessageFactory as _


def _registrations(context, comp):
    comp = removeSecurityProxy(comp)
    sm = component.getSiteManager(context)
    for meth, attrname in ((sm.registeredUtilities, 'component'),
                           (sm.registeredAdapters, 'factory'),
                           (sm.registeredSubscriptionAdapters, 'factory'),
                           (sm.registeredHandlers, 'factory')):
        for registration in meth():
            if getattr(registration, attrname) == comp or comp is None:
                yield registration

class IRegistrationDisplay(interface.Interface):
    """Display registration information
    """

    def id():
        """Return an identifier suitable for use in mapping
        """

    def render():
        "Return an HTML view of a registration object"

    def unregister():
        "Remove the registration by unregistering the component"

class ISiteRegistrationDisplay(IRegistrationDisplay):
    """Display registration information, including the component registered
    """

@component.adapter(None, zope.publisher.interfaces.browser.IBrowserRequest)
class RegistrationView(BrowserPage):

    render = zope.app.pagetemplate.ViewPageTemplateFile('registration.pt')

    def registrations(self):
        registrations = [
            component.getMultiAdapter((r, self.request), IRegistrationDisplay)
            for r in sorted(_registrations(self.context, self.context))
            ]
        return registrations

    def update(self):
        registrations = dict([(r.id(), r) for r in self.registrations()])
        for id in self.request.form.get('ids', ()):
            r = registrations.get(id)
            if r is not None:
                r.unregister()

    def __call__(self):
        self.update()
        return self.render()

@component.adapter(zope.component.interfaces.IUtilityRegistration,
                   zope.publisher.interfaces.browser.IBrowserRequest)
@interface.implementer(IRegistrationDisplay)
class UtilityRegistrationDisplay(object):
    """Utility Registration Details"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def provided(self):
        provided = self.context.provided
        return provided.__module__ + '.' + provided.__name__

    def id(self):
        joined = "%s %s" % (self.provided(), self.context.name)
        joined_bytes = joined.encode("utf8")
        j64_bytes = base64.b64encode(joined_bytes)
        if not isinstance(j64_bytes, str):
            j_str = j64_bytes.decode('ascii')
        else:
            j_str = j64_bytes
        escaped = j_str.replace('+', '_').replace('=', '').replace('\n', '')
        return 'R' + escaped

    def _comment(self):
        comment = self.context.info or ''
        if comment:
            comment = _("comment: ${comment}", mapping={"comment": comment})
        return comment

    def _provided(self):
        name = self.context.name
        provided = self.provided()
        if name:
            info = _("${provided} utility named '${name}'",
                     mapping={"provided": provided, "name": name})
        else:
            info = _("${provided} utility",
                     mapping={"provided": provided})
        return info

    def render(self):
        return {
            "info": self._provided(),
            "comment": self._comment()
            }

    def unregister(self):
        self.context.registry.unregisterUtility(
            self.context.component,
            self.context.provided,
            self.context.name,
            )

class SiteRegistrationView(RegistrationView):

    render = zope.app.pagetemplate.ViewPageTemplateFile('siteregistration.pt')

    def registrations(self):
        registrations = [
            component.getMultiAdapter((r, self.request),
                                      ISiteRegistrationDisplay)
            for r in sorted(_registrations(self.context, None))
            ]
        return registrations

@interface.implementer_only(ISiteRegistrationDisplay)
class UtilitySiteRegistrationDisplay(UtilityRegistrationDisplay):
    """Utility Registration Details"""

    def render(self):
        url = component.getMultiAdapter(
            (self.context.component, self.request), name='absolute_url')
        try:
            url = url()
        except TypeError: # pragma: no cover
            url = ""

        cname = getattr(self.context.component, '__name__', '')
        if not cname: # pragma: no cover
            cname = _("(unknown name)")
        if url:
            url += "/@@SelectedManagementView.html"

        return {
            "cname": cname,
            "url": url,
            "info": self._provided(),
            "comment": self._comment()
            }

@component.adapter(None, zope.publisher.interfaces.browser.IBrowserRequest)
class AddUtilityRegistration(form.Form):
    """View for registering utilities

    Normally, the provided interface and name are input.

    A subclass can provide an empty 'name' attribute if the component should
    always be registered without a name.

    A subclass can provide a 'provided' attribute if a component
    should always be registered with the same interface.

    """

    form_fields = form.Fields(
        schema.Choice(
           __name__ = 'provided',
           title=_("Provided interface"),
           description=_("The interface provided by the utility"),
           vocabulary="Utility Component Interfaces",
           required=True,
           ),
        schema.TextLine(
           __name__ = 'name',
           title=_("Register As"),
           description=_("The name under which the utility will be known."),
           required=False,
           default=u'',
           missing_value=u''
           ),
        schema.Text(
           __name__ = 'comment',
           title=_("Comment"),
           required=False,
           default=u'',
           missing_value=u''
           ),
        )

    name = provided = None

    prefix = 'field' # in hopes of making old tests pass. :)

    def __init__(self, context, request):
        if self.name is not None: # pragma: no cover
            self.form_fields = self.form_fields.omit('name')
        if self.provided is not None: # pragma: no cover
            self.form_fields = self.form_fields.omit('provided')
        super(AddUtilityRegistration, self).__init__(context, request)

    def update(self):
        # hack to make work with old tests
        if 'UPDATE_SUBMIT' in self.request.form: # pragma: no cover
            warnings.warn(
                "Old test needs to be updated.",
                DeprecationWarning)
            self.request.form['field.actions.register'] = 'Register'
            self.request.form['field.comment'] = u''
        super(AddUtilityRegistration, self).update()

    @property
    def label(self):
        return _("Register a $classname",
                 mapping=dict(classname=self.context.__class__.__name__)
                 )

    @form.action(_("Register"))
    def register(self, action, data):
        sm = component.getSiteManager(self.context)
        name = self.name
        if name is None:
            name = data['name']
        provided = self.provided
        if provided is None:
            provided = data['provided']

        # We have to remove the security proxy to save the registration
        sm.registerUtility(
            removeSecurityProxy(self.context),
            provided, name,
            data['comment'] or '')

        if 'UPDATE_SUBMIT' in self.request.form: # pragma: no cover
            # Backward compat until 3.5
            self.request.response.redirect('@@SelectedManagementView.html')
            return

        self.request.response.redirect('@@registration.html')
