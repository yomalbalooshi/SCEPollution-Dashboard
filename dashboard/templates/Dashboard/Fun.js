src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"
src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"
src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"
src="https://unpkg.com/amazon-quicksight-embedding-sdk@1.18.1/dist/quicksight-embedding-js-sdk.min.js"

$(function() {
    $('input[name="datepicker"]').daterangepicker({
      opens: 'left'
     }, function(start, end, label) {
  console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
   });
 });