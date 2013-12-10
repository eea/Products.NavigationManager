Introduction
============

This is a package that generates the portlet navigation for EEA Site

To generate a navigation portlet, the code does:

 * portlet template: navigation.pt
 * looks for adapters for INavigationSections for current context. In this
   way other sections can be defined by the context
 * with the list of sections, it calls python:view.createNavSection(section.value, section.title)
 * to render the section it uses the section.pt template
 * here it calls view.createNavTree(section=section)
