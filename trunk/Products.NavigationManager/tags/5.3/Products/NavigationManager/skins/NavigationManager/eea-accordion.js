jQuery(document).ready(function() {
  var portlet = jQuery('dl.portletNavigationTree');
  if(!portlet.length){
    return;
  }

  var tabs = jQuery('dd.portletItem', portlet);

  // Find current index
  var index = 0;
  tabs.each(function(idx, obj){
    var here = jQuery(this);
    if(jQuery('.navTreeCurrentNode', here).length > 0){
      index = idx;
      return false;
    }
  });

  // Make accordion using jquery.tools
  jQuery('dl.portletNavigationTree').tabs(
    "dl.portletNavigationTree dd.portletItem", {
    tabs: "dt.portletSubMenuHeader",
      effect: "slide",
      initialIndex: index
  });

  // Make current tab collapsible
  portlet.delegate('.current, .collapsed', 'click', function() {
    var tabs = portlet.data('tabs');
    if (index == tabs.getIndex()) {
      if(tabs.getCurrentTab().hasClass('current')){
        tabs.getCurrentPane().slideUp();
        tabs.getCurrentTab().removeClass('current').addClass('collapsed');
      }else{
        tabs.getCurrentPane().slideDown();
        tabs.getCurrentTab().addClass('current').removeClass('collapsed');
      }
    }
    index = tabs.getIndex();
  });

});
