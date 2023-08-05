webpackJsonp([1,0],[function(t,e,i){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}var n=i(22),o=s(n),a=i(2),l=(s(a),i(1)),r=(s(l),i(19)),c=s(r);o["default"].filter("capitalize",function(t){return"[object String]"===Object.prototype.toString.call(t)?t.charAt(0).toUpperCase()+t.slice(1):""}),o["default"].filter("camel",function(t){if("[object String]"===Object.prototype.toString.call(t)){for(var e="",i=t.split(/_/g),s=0;s<i.length;s++)e+=i[s].charAt(0).toUpperCase()+i[s].slice(1);return e}return""});new o["default"]({el:"body",components:{App:c["default"]}})},function(t,e,i){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}function n(t){var e,i,s=document.getElementById("canvas");t&&t.width&&t.height?(i=t.height*k.scale,e=t.width*i/t.height):(e=360,i=640),k.width=s.width=e,k.height=s.height=i,k.top=s.offsetTop,k.left=s.offsetLeft}function o(t){var e=document.getElementById("canvas"),i=e.getContext("2d");null==t?(i.font="30px Courier New",i.fillStyle="#aaa",i.fillRect(0,0,e.width,e.height),i.fillStyle="white",i.textAlign="center",i.fillText("没有图像",e.width/2,e.height/2)):(n(t),i.drawImage(t,0,0,e.width,e.height))}function a(){if(null!=_.current){for(var t=_.current-1,e=!1;t>=0;t--)if(!_.data[t].skip){e=!0;break}console.log("prevFrame",e,t),e&&(_.current=t)}}function l(){if(null!=_.current){for(var t=_.current+1,e=!1;t<_.data.length;t++)if(!_.data[t].skip){e=!0;break}e&&(_.current=t)}}function r(t){t<0||t>=_.data.length||(_.data[t].skip=!0)}function c(t){t<0||t>=_.data.length||(_.data[t].skip=!1)}function u(t,e){switch(t){case 1:return{left:e.top,top:w.width-e.left};case 2:return{left:w.width-e.left,top:w.height-e.top};case 3:return{left:w.height-e.top,top:e.left};default:return{left:e.left,top:e.top}}}function d(){h=new WebSocket("ws://"+location.host+"/run"),h.onopen=function(){console.log("WebSocket Closed")},h.onmessage=function(t){var e=JSON.parse(t.data);switch(e.action){case"run_all":_.current=e.frame,_.running&&e.frame<_.data.length-1?h.send((0,m["default"])({action:"run_all",frame:_.current+1})):_.running=!1;break;case"run_step":_.running=!1}},h.onerror=function(t){console.log(t)},h.onclose=function(){console.log("WebSocket Closed")}}function p(t){var e=function(){_.running=!0,t?h.send((0,m["default"])({action:"run_step",frame:_.current})):h.send((0,m["default"])({action:"run_all",frame:_.current}))};1!==h.readyState?(h.close(),d(),setTimeout(function(){e()},1e3)):e()}function f(){_.running=!1}var h,g=i(7),m=s(g),v=i(2),x=s(v),w={rotated:!1},y={data:{}},b={},_={data:[],current:null,running:!1,selected:{first:null,last:null}},k={show:!0,scale:.4,width:360,height:640,left:0,top:0};t.exports={device:w,frames:_,screenui:k,casesteps:y,logic:b,prevFrame:a,nextFrame:l,skipFrame:r,unskipFrame:c,drawImage:o,touchToScreen:u,saveCase:function(t){x["default"].ajax({url:"/case",method:"POST",data:{data:(0,m["default"])(t)},success:function(t){console.log(t)},dataType:"json"})},runCase:p,stopRunCase:f},(0,x["default"])(function(){x["default"].getJSON("/case/case.json",function(t){for(var e in t)t.hasOwnProperty(e)&&(y.data[e]=t[e]);x["default"].getJSON("/frames/frames.json",function(t){var e;for(e in t.device)w[e]=t.device[e];if(w.width>=1080?k.scale=.4:w.width>=540?k.scale=.8:k.scale=1,n(w),t.frames.length>0){for(var i,s=0,o=t.frames.length;s<o;s++)i=t.frames[s],i.skip=void 0==y.data[s+""],_.data.push(i);setTimeout(function(){_.current=0},1e3)}})}),(0,x["default"])(document).keydown(function(t){switch(t.keyCode){case 37:return a(),!1;case 39:return l(),!1}}),(0,x["default"])(window).resize(function(){if(null!=_.current){var t=_.data[_.current];o(t.$vm.img)}else n(w)}),d()})},,function(t,e,i){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var n=i(2),o=s(n),a=i(1),l=s(a);e["default"]={props:{idx:{required:!0,coerce:function(t){return parseInt(t)}}},data:function(){return{uilayer:l["default"].screenui,frames:l["default"].frames,casesteps:l["default"].casesteps,scale:.4,img:{instance:null,width:null,height:null,src:null},action:null,action_options:[],action_changing:!1,xml:null,key:null,point:{left:void 0,top:void 0},uinodes:[],selected_node:null,imgbound:{left:0,top:0,width:0,height:0},imgdragging:!1,imgresizing:!1,swipepoints:null}},computed:{icon:function(){return"/static/imgs/"+this.action+".png"},frameclass:{cache:!1,get:function(){var t=null!=this.frames.selected.first&&null!=this.frames.selected.last;return{highlight:this.idx==this.frames.current,skipped:1==this.frames.data[this.idx].skip,selected:t&&this.idx>=this.frames.selected.first&&this.idx<=this.frames.selected.last}}},chopstyle:function(){var t=50,e=t/this.imgbound.height,i=this.imgbound.width*e,s=this.imgbound.left*e,n=this.imgbound.top*e,o=this.img.width*e,a=this.img.height*e;return{height:t+"px",width:i+"px","background-image":"url("+this.img.src+")","background-position":"-"+s+"px -"+n+"px","background-size":o+"px "+a+"px"}},overlapstyle:function(){var t=this.$el.offsetParent,e=t?t.offsetTop:0,i=t?t.offsetLeft:0;return{display:this.idx==this.frames.current?"block":"none",position:"absolute",left:this.uilayer.left-i+"px",top:this.uilayer.top-e+"px",width:this.uilayer.width+"px",height:this.uilayer.height+"px"}},pointstyle:function(){var t=18,e=this.point.left*this.uilayer.scale-.5*t,i=this.point.top*this.uilayer.scale-.5*t;return{width:t+"px",height:t+"px","border-radius":t+"px",position:"absolute",left:e+"px",top:i+"px"}},rectstyle:function(){var t=this.imgbound.left*this.uilayer.scale,e=this.imgbound.top*this.uilayer.scale,i=this.imgbound.width*this.uilayer.scale,s=this.imgbound.height*this.uilayer.scale;return{width:i+"px",height:s+"px",left:t+"px",top:e+"px"}},uiboxstyle:function(){var t=this.selected_node;return void 0==t?{}:{top:t.top*this.uilayer.scale+"px",left:t.left*this.uilayer.scale+"px",width:t.width*this.uilayer.scale+"px",height:t.height*this.uilayer.scale+"px"}}},created:function(){var t=this,e=t.frames.data[t.idx],i=this.frames.data[this.idx].status.rotation;e.$vm=t,e.status.screen&&(t.img.instance=new Image,t.img.instance.src="/frames/"+e.status.screen,t.img.instance.addEventListener("load",function(){t.img.src=this.src,t.img.width=this.width,t.img.height=this.height}));var s=t.casesteps.data[t.idx+""];if(s?t.action=s.action:t.action=e.event.action,"click"==t.action.substr(0,5)){t.action_options.push("click"),t.action_options.push("click_ui"),t.action_options.push("click_image");var n=l["default"].touchToScreen(i,{left:e.event.args[0],top:e.event.args[1]});t.point.left=n.left,t.point.top=n.top}else t.action_options.push(t.action);if("click_ui"==t.action);else if("click_image"==t.action){var a=s.args[2];t.imgbound.left=a[0],t.imgbound.top=a[1],t.imgbound.width=a[2],t.imgbound.height=a[3]}else"swipe"==t.action?(t.swipepoints={start:l["default"].touchToScreen(i,{left:e.event.args[0],top:e.event.args[1]}),end:l["default"].touchToScreen(i,{left:e.event.args[2],top:e.event.args[3]})},t.point.left=e.event.args[0],t.point.top=e.event.args[1]):"key_event"==t.action&&(t.key=e.event.args[0]);e.status.uixml&&void 0!=this.point.left&&o["default"].ajax({url:"/frames/"+e.status.uixml,type:"GET",dataType:"xml",success:function(e){var i=0;(0,o["default"])(e).find("node").each(function(){var e=(0,o["default"])(this),s=i;i+=1;var n=e.attr("bounds").match(/\d+/g),a=parseInt(n[0]),r=parseInt(n[1]),c=parseInt(n[2]),u=parseInt(n[3]),d=c-a,p=u-r;if((d!=l["default"].device.width||p!=l["default"].device.height)&&!(t.point.left<a||t.point.left>c||t.point.top<r||t.point.top>u)){var f={left:a,top:r,right:c,bottom:u,width:d,height:p,iterindex:s,xml:e};f.info={className:e.attr("class"),resourceId:e.attr("resource-id"),text:e.attr("text"),description:e.attr("content-desc")},t.uinodes.push(f)}}),"click_ui"==t.action&&t.uinodes.length>0&&(t.selected_node=t.uinodes[t.uinodes.length-1])},error:function(){console.log("Get uixml failed",e.status.uixml),t.uinodes=[]}})},methods:{select:function(){var t=this.frames.selected;console.log("on select",this.idx,t),null==t.first||null==t.last?(t.first=this.idx,t.last=this.idx):this.idx<t.first?t.first=this.idx:this.idx>t.last?t.last=this.idx:t.first=t.last=null},skip:function(t){t.stopPropagation(),this.frames.data[this.idx].skip=!0},unskip:function(t){t.stopPropagation(),this.frames.data[this.idx].skip=!1},changeAction:function(t){this.action_options.length<=1||("click_ui"==self.action&&null==self.selected_node&&self.uinodes.length>0&&(self.selected_node=self.uinodes[self.uinodes.length-1]),this.action_changing=!0)},doneChangeAction:function(t){this.action_changing=!1,console.log("action changed",this.idx,this.action)},uinodeDesc:function(t){return""!=t.info.text?t.info.text:""!=t.info.description?t.info.description:""!=t.info.resourceId?t.info.resourceId:t.info.className},showMe:function(t){this.unskip(t),this.frames.current=this.idx},startRect:function(t){this.imgdragging=!0,this.imgbound.left=parseInt((t.pageX-this.uilayer.left)/this.uilayer.scale),this.imgbound.top=parseInt((t.pageY-this.uilayer.top)/this.uilayer.scale)},drawRect:function(t){if(this.imgdragging||this.imgresizing){var e=parseInt((t.pageX-this.uilayer.left)/this.uilayer.scale),i=parseInt((t.pageY-this.uilayer.top)/this.uilayer.scale);this.imgbound.width=Math.min(600,Math.max(60,e-this.imgbound.left)),this.imgbound.height=Math.min(600,Math.max(60,i-this.imgbound.top))}},stopRect:function(t){this.imgdragging&&(this.imgdragging=!1),this.imgresizing&&(this.imgresizing=!1)},outRect:function(t){(this.imgdragging||this.imgresizing)&&(t.pageX<this.uilayer.left||t.pageX>this.uilayer.left+this.uilayer.width||t.pageY<this.uilayer.top||t.pageY>this.uilayer.top+this.uilayer.height)&&(this.imgdragging=!1,this.imgresizing=!1)},startResize:function(t){t.stopPropagation(),this.imgresizing=null==self.selected_node}},components:{},watch:{"frames.current":function(t,e){t==this.idx&&l["default"].drawImage(this.img.instance)}}}},function(t,e,i){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var n=i(2),o=(s(n),i(1)),a=s(o),l=i(20),r=s(l),c=i(18),u=s(c),d=i(21),p=s(d);e["default"]={data:function(){return{frames:a["default"].frames,casesteps:a["default"].casesteps,screenui:a["default"].screenui,show_toolbar:!1}},components:{Scroll:r["default"],ActionFrame:u["default"],Toolbar:p["default"]},methods:{saveCase:function(){for(var t,e,i,s,n=this.$refs.allframes,o=[],l=0,r=this.frames.data.length;l<r;l++)e=this.frames.data[l],1!=e.skip&&(i=n.$children[l],t={frameidx:l,action:i.action,args:[]},"click_image"==i.action?(s=[i.imgbound.left,i.imgbound.top,i.imgbound.width,i.imgbound.height],t.args=[i.point.left,i.point.top,s]):"click_ui"==i.action?t.args=[i.selected_node.iterindex]:t.args=e.event.args,o.push(t));a["default"].saveCase(o)},toggleToolbar:function(){this.show_toolbar=!this.show_toolbar},runCase:function(){a["default"].runCase()},stopRunCase:function(){a["default"].stopRunCase()},runCaseStep:function(){a["default"].runCase(!0)}}}},function(t,e,i){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var n=i(1),o=s(n);e["default"]={data:function(){return{frames:o["default"].frames,top_more:!1,bottom_more:!1,scrollnode:null}},computed:{},methods:{onScroll:function(t){if(!this.scrollnode)for(var e,i=0,s=this.$el.children.length;i<s;i++)if(e=this.$el.children[i],"scroll"==e.className){this.scrollnode=e;break}if(this.scrollnode){var n=this.scrollnode;this.top_more=0!=n.scrollTop,this.bottom_more=n.scrollTop+n.clientHeight!=n.scrollHeight}}}}},function(t,e,i){"use strict";function s(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var n=i(1),o=s(n);e["default"]={data:function(){return{frames:o["default"].frames,tools:{skipFrames:{icon:"/static/imgs/1_touch.png"},replaceWithOpenApp:{icon:"/static/imgs/open.png"}}}},computed:{},ready:function(){},attached:function(){},methods:{click:function(t){var e=this[t];e&&(console.log("calling",t),e.call(this))},skipFrames:function(){var t=this.frames.selected;if(null!=t.first&&null!=t.last){for(var e=t.first;e<=t.last;e++)this.frames.data[e].skip=!0;t.first=t.last=null}},replaceWithOpenApp:function(){var t=this.frames.selected,e=t.first,i=t.last;null!=e&&null!=i||(e=i=this.frames.current)}},components:{}}},,,,function(t,e){},function(t,e){},function(t,e){},function(t,e){},function(t,e){t.exports=' <div class="frame clear-fix" :class=frameclass @click=showMe> <div class=left> <img :src=icon @click=select /> <span style=position:relative> <b @click=changeAction v-show=!action_changing>{{ action | camel }}</b> <select v-show=action_changing v-model=action @change=doneChangeAction style=overflow-y:hidden :size=action_options.length> <option v-for="opt in action_options">{{opt}}</option> </select> </span> <template v-if="(action==\'key_event\')"> <span>{{key}}</span> </template> <template v-if="(action==\'click_ui\')"> <select v-model=selected_node> <option v-for="node in uinodes" :value=node> {{node.iterindex}} {{uinodeDesc(node)}} </option> </select> </template> <template v-if="(action==\'click_image\')"> <div class=chop :style=chopstyle></div> <span>({{imgbound.width}}x{{imgbound.height}})@({{imgbound.left}}, {{imgbound.top}})</span> </template> <template v-if="(action==\'click\')"> <span>({{point.left}}, {{point.top}})</span> </template> <template v-if="(action==\'swipe\')"> <span>From ({{swipepoints.start.left}}, {{swipepoints.start.top}}) To ({{swipepoints.end.left}}, {{swipepoints.end.top}})</span> </template> </div> <div class=right> <button class=skip @click=skip></button> </div> <div class=uioverlap :style=overlapstyle> <div class=full> <template v-if=uilayer.show> <template v-if="(action.substr(0,5)==\'click\')"> <div class=point :style=pointstyle></div> </template> <template v-if="(action.substr(0,5)==\'swipe\')"> <svg xmlns=http://www.w3.org/2000/svg width=100% height=100%> <defs> <linearGradient id=swipestroke x1=0% y1=0% x2=100% y2=100%> <stop offset=0% style=stop-color:rgb(255,255,255);stop-opacity:0.1 /> <stop offset=100% style=stop-color:rgb(255,255,255);stop-opacity:0.8 /> </linearGradient> <filter id=swipefilter x=0 y=0 width=100% height=100%> <feGaussianBlur in=SourceGraphic stdDeviation=2 /> </filter> </defs> <line :x1=swipepoints.start.left*scale :y1=swipepoints.start.top*scale :x2=swipepoints.end.left*scale :y2=swipepoints.end.top*scale style=stroke:url(#swipestroke);stroke-width:20;stroke-linecap:round /> <circle :cx=swipepoints.start.left*scale :cy=swipepoints.start.top*scale r=10 fill=white /> <circle :cx=swipepoints.end.left*scale :cy=swipepoints.end.top*scale r=10 fill=white fill-opacity=0.2 /> </svg> </template> </template> <template v-if="(action==\'click_ui\')"> <div class=uibox :style=uiboxstyle></div> </template> <template v-if="(action==\'click_image\')"> <div class=full @mousedown=startRect @mouseup=stopRect @mouseout=outRect @mousemove=drawRect> <div class=rect v-bind:style=rectstyle> <div class=resizer @mousedown=startResize></div> </div> </div> </template> </div> </div> </div> '},function(t,e){t.exports=' <div id=app class=wrapper> <div v-show=show_toolbar class=toolbar> <toolbar></toolbar> </div> <div class=left-panel> <div> <ul> <li><button @click=saveCase>Save</button></li> <li v-if=frames.running><button @click=stopRunCase>Stop</button></li> <li v-else><button @click=runCase>Run</button></li> <li><button @click=runCaseStep>RunStep</button></li> <li>Current Frame: {{frames.current + 1}}/{{frames.data.length}}</li> <li>Show Actions:<input type=checkbox v-model=screenui.show /></li> </ul> </div> <div style=height:90%> <scroll v-ref:allframes> <action-frame v-for="idx in frames.data.length" :idx=idx></action-frame> </scroll> </div> </div> <div class=right-panel> <canvas id=canvas width=300 height=300></canvas> </div> </div> '},function(t,e){t.exports=" <div class=scroll-wrapper> <div v-if=top_more class=scroll-top-more> <div class=arrow-up></div> </div> <div class=scroll @scroll=onScroll> <slot></slot> </div> <div v-if=bottom_more class=scroll-bottom-more> <div class=arrow-down></div> </div> </div> "},function(t,e){t.exports=' <div> <div class=tool v-for="t in tools"> <button type=button @click=click($key)> <img :src=t.icon alt={{$key}} /> </button> </div> </div> '},function(t,e,i){var s,n;i(10),s=i(3),n=i(14),t.exports=s||{},t.exports.__esModule&&(t.exports=t.exports["default"]),n&&(("function"==typeof t.exports?t.exports.options||(t.exports.options={}):t.exports).template=n)},function(t,e,i){var s,n;i(11),s=i(4),n=i(15),t.exports=s||{},t.exports.__esModule&&(t.exports=t.exports["default"]),n&&(("function"==typeof t.exports?t.exports.options||(t.exports.options={}):t.exports).template=n)},function(t,e,i){var s,n;i(12),s=i(5),n=i(16),t.exports=s||{},t.exports.__esModule&&(t.exports=t.exports["default"]),n&&(("function"==typeof t.exports?t.exports.options||(t.exports.options={}):t.exports).template=n)},function(t,e,i){var s,n;i(13),s=i(6),n=i(17),t.exports=s||{},t.exports.__esModule&&(t.exports=t.exports["default"]),n&&(("function"==typeof t.exports?t.exports.options||(t.exports.options={}):t.exports).template=n)}]);