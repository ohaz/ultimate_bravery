$(document).ready(function() {
    var copyTextareaBtn = document.querySelector('.js-textareacopybtn');
    var copyTextareaBtn2 = document.querySelector('.js-textareacopybtn2');
    var copyTextarea = document.querySelector('.js-copytextarea');
    var host = location.protocol + '//' + location.host;
    copyTextarea.value = host + copyTextarea.value;
    //console.log(copyTextarea.value);

    copyTextareaBtn.addEventListener('click', function(event) {
      copyTextarea.select();

      try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copying text command was ' + msg);
      } catch (err) {
        console.log('Oops, unable to copy');
      }
    });

    copyTextareaBtn2.addEventListener('click', function(event) {
      copyTextarea.select();

      try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        //console.log('Copying text command was ' + msg);
      } catch (err) {
        //console.log('Oops, unable to copy');
      }
    });
});
