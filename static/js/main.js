$('#categories')
  .popup({
    inline   : true,
    hoverable: true,
    position : 'bottom left',
    delay: {
      show: 50,
      hide: 100
    }
  })
;

// $('#post_listing')
//   .dropdown({
//     on: 'hover'
//   })
// ;

$('.ui.dropdown')
  .dropdown()
;

$('#user')
  .dropdown({
    on: 'hover'
  })
;

$('.ui.checkbox')
  .checkbox()
;

$('.sidebar').first()
  .sidebar('setting', 'transition', 'overlay')
  .sidebar('attach events', '.menu-button')
;


