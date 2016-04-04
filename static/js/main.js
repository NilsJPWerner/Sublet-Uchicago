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

$('#bug').click(function(){
  event.preventDefault();
  $('#bug-modal').modal({})
  .modal('show');
});


$('#bug-form')
  .form({
    fields: {
      email: {
        identifier: 'bug-email',
        rules: [
          {
            type   : 'email',
            prompt : 'Please enter your email address'
          }
        ]
      },
      report: {
        identifier: 'bug-report',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter a description of the bug'
          }
        ]
      },
    },
    onSuccess : function(){
        event.preventDefault();
        var formData = {
          'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
          'email'               : $('input[name=bug-email]').val(),
          'report'              : $('textarea[name=bug-report]').val(),
          'contactme'           : $('input[name=bug-contactme]').val()
        };
        $.ajax({
            type        : 'POST',
            url         : '/bug-report/',
            data        : formData,
            beforeSend  : function(){
              $("#bug-report-send").addClass("loading");
            },
            success     : function(data) {
              $("#bug-report-send").removeClass("loading");
              $('#bug-form').form('clear');
              $('#bug-modal').modal('hide');
            },
            error       : function(xhr,errmsg,err) {
              $("#bug-report-send").removeClass("loading");
              console.log("failure");
              $('#bug-form').form('add errors', ["Something went wrong, please try again later"]);
            }
        });
    }
  })
;


$('#contact').click(function(){
  event.preventDefault();
  $('#contact-modal').modal({})
  .modal('show');
});


$('#contact-form')
  .form({
    fields: {
      email: {
        identifier: 'contact-email',
        rules: [
          {
            type   : 'email',
            prompt : 'Please enter your email address'
          }
        ]
      },
      subject: {
        identifier: 'contact-subject',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter a subject'
          }
        ]
      },
      message: {
        identifier: 'contact-message',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter a message'
          }
        ]
      },
    },
    onSuccess : function(){
        event.preventDefault();
        var formData = {
          'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
          'name'                : $('input[name=contact-name]').val(),
          'email'               : $('input[name=contact-email]').val(),
          'subject'               : $('input[name=contact-subject]').val(),
          'message'              : $('textarea[name=contact-message]').val(),
        };
        $.ajax({
            type        : 'POST',
            url         : '/contact/',
            data        : formData,
            beforeSend  : function(){
              $("#contact-send").addClass("loading");
            },
            success     : function(data) {
              $("#contact-send").removeClass("loading");
              $('#contact-form').form('clear');
              $('#contact-modal').modal('hide');
            },
            error       : function(xhr,errmsg,err) {
              $("#contact-send").removeClass("loading");
              console.log("failure");
              $('#contact-form').form('add errors', ["Something went wrong, please try again later"]);
            }
        });
    }
  })
;


