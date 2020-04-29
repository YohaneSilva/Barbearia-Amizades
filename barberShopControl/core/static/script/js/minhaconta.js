(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

})(jQuery); // End of use strict

// Pegar o id do registro 
$('td #btnEditService').click(function () {
  var $idSelectedItem = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#codeService")     // Gets a descendent with class="#codeService"
    .text();         // Retrieves the text within <td>
  
  var url = 'http://127.0.0.1:8000/minhaconta/servicos/'+$idSelectedItem+'/editar';

  window.open(url);
});

// Refresh da tabela de serviços
$(document).ready(function (){
  $("#btnRefreshTableService").click(function(){
      location.reload(true);
  });
});

// Retornar ao topo da página
$("#backToTop").click(function () {
  $("html, body").animate({scrollTop: 0}, 1000);
});

// Contador das linhas da tabela
$(document).ready(function () {
  var quantidadeLinhasTabela = $('#tableService tr').length - 1;
  $('#lengthRowTableService').html('<strong>Quantidade de Serviços Cadastrados: </strong> '+quantidadeLinhasTabela);
});

