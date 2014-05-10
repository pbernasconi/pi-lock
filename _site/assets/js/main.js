


var ionicSite = function() {
  var smoothScrollingTo,
    fixedMenu,
    winHeight = $(window).height(),
    docContent = $('.main-content'),
    devicePreview,
    defaultScreen;


  // left menu link highlight
  var leftMenu = $('.left-menu');
  var activeLink = leftMenu.find('[href="' + window.location.pathname + '"]');
  activeLink.parents('ul').addClass('active-menu');
  activeLink.parents('li').addClass("active");


  console.log(activeLink);



  leftMenu.find('.api-section').click(function(){
    if( $(this).attr('href') == '#' ) {
      $(this).closest('.left-menu').find("li").removeClass('active');
      $(this).closest('li').toggleClass('active');
      return false;
    }
  });


  (function() {
    var activeId;
    fixedMenu = $('.docked-menu');
    if(fixedMenu.length) {

      var targets = fixedMenu.find('.active-menu').find('a');
      targets.each(function() {
        var href = $(this).attr('href');
        if(href && href.indexOf('#') > -1) {
          href = href.split('#');
          href = "#" + href[ href.length - 1 ];
          $(this).attr('href', href);
        }
      });

      var scrollSpyOffset = 40;
      if( $(document.body).hasClass("device-preview-page") ) {
        scrollSpyOffset = 300;
      }

      $(document.body).scrollspy({ target: '.docked-menu', offset: scrollSpyOffset });

      var fixedMenuTop = fixedMenu.offset().top;
      var menuTopPadding = 20;
      fixedMenu.css({
        top: menuTopPadding + 'px'
      });

      function docScroll() {
        var win = $(window);
        var scrollTop = win.scrollTop();
        var winWidth = win.width();
        if(scrollTop + menuTopPadding > fixedMenuTop && winWidth >= 768) {
          // middle of the page
          if(!fixedMenu.hasClass("fixed-menu")) {
            fixedMenu
              .css({
                width: fixedMenu.width() + 'px',
                top: '20px'
              })
              .addClass("fixed-menu");
          }
        } else {
          // top of page
          if(fixedMenu.hasClass("fixed-menu")) {
            fixedMenu
              .removeClass("fixed-menu")
              .css({
                width: 'auto',
                top: '20px'
              });
          }
          if(scrollTop < 200) {
            $('.active').removeClass(".active");
          }
        }
      }
      $(window).resize(function() {
        //preFooterTop = $('.pre-footer').offset().top;
        winHeight = $(window).height();
        fixedMenu
          .removeClass("fixed-menu")
          .css({
            width: 'auto'
          });
        docScroll();
      });
      var docScrollGovernor;
      function governDocScroll(){
        clearTimeout(docScrollGovernor);
        docScrollGovernor = setTimeout(docScroll, 15);
      }
      $(window).scroll(governDocScroll);

      function scrollSpyChange(e) {
        if(smoothScrollingTo || !docContent) {
          window.history.replaceState && window.history.replaceState({}, smoothScrollingTo, smoothScrollingTo);
          return;
        }

        var id;
        if(e.target.children.length > 1) {
          // this is a top level nav link
          var activeSublinks = $(e.target).find('.active');
          if(!activeSublinks.length) {
            // no children are active for this top level link
            id = e.target.children[0].hash;
          }
        } else if(e.target.children.length === 1) {
          // this is a sub nav link
          id = e.target.children[0].hash;
        }

        if(id) {
          if(devicePreview) {
            window.rAF(function(){
              previewSection(id);
            });
          } else {
            var activeSection = $(id);
            if(activeSection.length) {
              window.rAF(function(){
                docContent.find('.active').removeClass('active');
                activeSection.addClass("active");
              });
            }
          }
          window.history.replaceState && window.history.replaceState({}, id, id);
        }
      }
      fixedMenu.on('activate.bs.scrollspy', scrollSpyChange);
    }
  })();



}();
