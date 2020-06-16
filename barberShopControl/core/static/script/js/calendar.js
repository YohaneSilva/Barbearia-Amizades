$(function () {
  var dateFormat = $(".datepicker").datepicker("option", "dateFormat");

  // Setter
  $(".datepicker").datepicker("option", "dateFormat", "yy-mm-dd");
  $(".datepicker").datepicker({ dateFormat: "dd-mm-yy" }).val();

  $("#datepicker").datepicker({
    prevText: '<i class="fa fa-fw fa-angle-left"></i>',
    nextText: "Próximo>",
    language: "pt-BR",
  });
});
