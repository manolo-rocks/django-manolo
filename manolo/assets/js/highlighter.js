/*

highlight v4

Highlights arbitrary terms.

<http://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html>

MIT license.

Johann Burkard
<http://johannburkard.de>
<mailto:jb@eaio.com>

*/

!function($){$.fn.highlight=function(e,t){function n(e){var t=[[/[\u00c0-\u00c6]/g,"A"],[/[\u00e0-\u00e6]/g,"a"],[/[\u00c7]/g,"C"],[/[\u00e7]/g,"c"],[/[\u00c8-\u00cb]/g,"E"],[/[\u00e8-\u00eb]/g,"e"],[/[\u00cc-\u00cf]/g,"I"],[/[\u00ec-\u00ef]/g,"i"],[/[\u00d1|\u0147]/g,"N"],[/[\u00f1|\u0148]/g,"n"],[/[\u00d2-\u00d8|\u0150]/g,"O"],[/[\u00f2-\u00f8|\u0151]/g,"o"],[/[\u0160]/g,"S"],[/[\u0161]/g,"s"],[/[\u00d9-\u00dc]/g,"U"],[/[\u00f9-\u00fc]/g,"u"],[/[\u00dd]/g,"Y"],[/[\u00fd]/g,"y"]];for(var n=0;n<t.length;n++){e=e.replace(t[n][0],t[n][1])}return e}function r(e,t,i){var s=0;if(e.nodeType==3){var o=$.isArray(t);if(!o){t=[t]}var u=t.length;for(var a=0;a<u;a++){var f=(i?n(t[a]):t[a]).toUpperCase();var l=(i?n(e.data):e.data).toUpperCase().indexOf(f);if(l>=0){var c=document.createElement("span");c.className="highlight";var h=e.splitText(l);var p=h.splitText(f.length);var d=h.cloneNode(true);c.appendChild(d);h.parentNode.replaceChild(c,h);s=1}}}else if(e.nodeType==1&&e.childNodes&&!/(script|style)/i.test(e.tagName)){for(var v=0;v<e.childNodes.length;++v){v+=r(e.childNodes[v],t,i)}}return s}return this.length&&e&&e.length?this.each(function(){t=typeof t!=="undefined"?t:$.fn.highlight.defaults.ignore;r(this,e,t)}):this};$.fn.highlight.defaults={ignore:false};$.fn.removeHighlight=function(){return this.find("span.highlight").each(function(){this.parentNode.firstChild.nodeName;with(this.parentNode){replaceChild(this.firstChild,this);normalize()}}).end()}}(window.jQuery)
