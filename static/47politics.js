jQuery(function($){

var _ua = (function(){
 return {
  ltIE6:typeof window.addEventListener == "undefined" && typeof document.documentElement.style.maxHeight == "undefined",
  ltIE7:typeof window.addEventListener == "undefined" && typeof document.querySelectorAll == "undefined",
  ltIE8:typeof window.addEventListener == "undefined" && typeof document.getElementsByClassName == "undefined",
  mobile:/android|iphone|ipad|ipod/i.test(navigator.userAgent.toLowerCase())
 }
})();

if(!_ua.ltIE8){

    $(function(){
    $(".shuyou_box, .shinchaku_box, .schedule_box, .local_box").mCustomScrollbar({
          theme:"light",
          scrollInertia:0,
          mouseWheelPixels:19,
          snapAmount:19,
          snapOffset: 1,
          scrollButtons:{
          enable:true,
          scrollType:"pixels",
          scrollAmount:19
          }
        });
    });

}else if(_ua.ltIE7){

}
// トップページの特集と新着ニュースのdlのクリック設定
$('.shuyou_box dl, .shinchaku_box dl').click(function(){
  window.location = ($(this).find('a').attr('href'));
  return false;
});
// 動画ページのフロート用（IE6~8対策）
$(".movie_list .thumnail_box:nth-child(odd)").css("margin-right","10px");

// 政治家データペースのリストページ用（IE6~8対策）
$(".db_list .thumnail_box:nth-child(3n)").css("margin-right","0px");

});

// 地域政治ニュースの新聞社選択時
function reScroll(){
  var _ua = (function(){
 return {
  ltIE6:typeof window.addEventListener == "undefined" && typeof document.documentElement.style.maxHeight == "undefined",
  ltIE7:typeof window.addEventListener == "undefined" && typeof document.querySelectorAll == "undefined",
  ltIE8:typeof window.addEventListener == "undefined" && typeof document.getElementsByClassName == "undefined",
  mobile:/android|iphone|ipad|ipod/i.test(navigator.userAgent.toLowerCase())
 }
})();

if(!_ua.ltIE8){

    $(function(){
    $(".local_box").mCustomScrollbar({
          theme:"light",
          scrollInertia:0,
          mouseWheelPixels:19,
          snapAmount:19,
          snapOffset: 1,
          scrollButtons:{
          enable:true,
          scrollType:"pixels",
          scrollAmount:19
          }
        });
    });

}else if(_ua.ltIE7){

}

}