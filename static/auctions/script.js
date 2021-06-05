(function () {

  // Toggle button for mobile view 
  $("#mobileToggleBtn").on("click", function(){
    $(".navbar-nav").toggle(1000);
  });

  // close notification button
  $("#closebtn").on("click", function(){
    $("#alert").hide(1000);
  });

  // Active route links
  const route = window.location.pathname;
  const target = $('.nav-item a[href= "'+route+'"]');
  const auth = $('.nav-auth a[href= "'+route+'"]'); 
  const catagory = ($('.dropdown-menu a[href= "'+route+'"]').parent()).parent();
  const footerLinks = $('footer a[href= "'+route+'"]'); 
  footerLinks.addClass('footerLinksActive');
  target.addClass('active');
  auth.addClass('active');
  catagory.addClass('active');

}());