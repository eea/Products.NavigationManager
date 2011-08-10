jQuery(document).ready(function() {
  var portlet = jQuery('dl.portletNavigationTree');
  if(!portlet.length){
    return;
  }

  var tabs = jQuery('dd.portletItem', portlet);
  var index = 0;

  tabs.each(function(idx, obj){
    var here = jQuery(this);
    if(jQuery('.navTreeCurrentNode', here).length > 0){
      index = idx;
      return false;
    }
  });

  jQuery('dl.portletNavigationTree').tabs(
    "dl.portletNavigationTree dd.portletItem", {
    tabs: "dt.portletSubMenuHeader",
      effect: "slide",
      initialIndex: index
  });
});
