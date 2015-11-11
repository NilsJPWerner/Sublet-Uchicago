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

$('#post_listing')
  .dropdown({
    on: 'hover'
  })
;

$('#user')
  .dropdown({
  	on: 'hover'
  })
;