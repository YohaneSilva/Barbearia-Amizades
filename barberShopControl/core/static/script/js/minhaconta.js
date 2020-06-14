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


// Editar Serviço: Pegar o id do registro do Serviço e enviar para a view
$('td #btnEditarServico').click(function () {
  var $idSelectedItem = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#codeService")     // Gets a descendent with id="codeService"
    .text();         // Retrieves the text within <td>
  
  var url = 'http://127.0.0.1:8000/minha-conta/servicos/'+$idSelectedItem+'/editar';

  window.location.href = url;
});

// Excluir Serviço: Pegar o id do registro do Serviço e enviar para a view
$('td #btnEditarSituacaoServico').click(function () {
  var $idSelectedItem = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#codeService")     // Gets a descendent with id="codeService"
    .text();         // Retrieves the text within <td>
  
  var url = 'http://127.0.0.1:8000/minha-conta/servicos/'+$idSelectedItem+'';

  window.location.href = url;
});


// Editar Usuário: Pegar o id do registro do Usuário e enviar para  view
$('td #btnEditUser').click(function () {
  var $idSelectedItem = $(this) 
    .closest("tr")   // Finds the closest row <tr> 
    .find("#codeUser")     // Gets a descendent with id="codeUser"
    .text();         // Retrieves the text within <td>
  
  var url = 'http://127.0.0.1:8000/minha-conta/conta/'+$idSelectedItem+'/editar';

  window.location.href = url;
});

// Refresh da tabela de serviços
$(document).ready(function (){
  $("#btnRefreshPage").click(function(){
      location.reload(true);
  });
});

// Retornar ao topo da página
$("#backToTop").click(function () {
  $("html, body").animate({scrollTop: 0}, 1000);
});

// Contador das linhas da tabela
$(document).ready(function () {
  var quantidadeLinhasTabela = $('#tableAllResults tr').length - 2;
  var quantidadeLinhasTabelaServico = $('#tableAllResultsService tr').length - 1;

  $('#lengthRowTable').html('<strong>Quantidade de Registros: </strong> '+quantidadeLinhasTabela);
  $('#lengthRowTableService').html('<strong>Quantidade de Registros: </strong> '+quantidadeLinhasTabelaServico);

  // Remover classe da tabela quando acessado pelo mobile
  var tamanhoJanela = $( window ).width();
  if (tamanhoJanela <= 768) {
    $("#listingTable").removeClass("container-fluid");
    $("#tableAllResults").removeClass("container-fluid");
  };
});

// Habilitar o modal de Cancelamento e Finalizar Atendimento 
// através do clique no botão Mais Informações
$('td #btnMaisInformacoes').click(function () {
  var idAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#codeBooking")     // Gets a descendent with id="codeService"
    .text();

  var dataAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#dataAtendimento")     // Gets a descendent with id="codeService"
    .text();
  
  var nomeCliente = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#nomeCliente")     // Gets a descendent with id="codeService"
    .text();

  var periodoAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#periodoAtendimento")     // Gets a descendent with id="codeService"
    .text();
  
  var agendadoEm = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#agendadoEm")     // Gets a descendent with id="codeService"
    .text();
    
  var statusAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#statusAtendimento")     // Gets a descendent with id="codeService"
    .text();
  
  var emailCliente = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#emailCliente")     // Gets a descendent with id="codeService"
    .text();

  var observacaoCliente = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#observacaoCliente")     // Gets a descendent with id="codeService"
    .text();

  $('#maisInformacoesDataAtendimento').html(dataAtendimento);
  $('#maisInformacoesNomeCliente').html(nomeCliente);
  $('#maisInformacoesPeriodoAtendimento').html(periodoAtendimento);
  $('#maisInformacoesAgendadoEm').html(agendadoEm);
  $('#maisInformacoesStatusAtendimento').html(statusAtendimento);
  $('#maisInformacoesObservacaoCliente').html(observacaoCliente);
  $('#idRegistro').attr('value', idAtendimento);
  $('#idRegistroObservacao').attr('value', idAtendimento);
  $('#nomeCliente').attr('value', nomeCliente);
  $('#dataAgendada').attr('value', dataAtendimento);
  $('#emailCliente').attr('value', emailCliente);
  $('#observacaoCliente').attr('value', emailCliente);

  if(statusAtendimento == 'Finalizado' || statusAtendimento == 'Cancelado'){
    $('#formFinalizarCancelar').hide();
  } else {
    $('#formFinalizarCancelar').show();
  }

  $('#modalMaisInformacoes').modal('show');
});

// Habilitar modal de Cancelamento e Finalizar Atendimento 
// e modal de Avaliação do Cliente
// com duplo clique na linha de registro
$(document).ready(function (){
  $('#tableAllResults td').dblclick(function (){
    var idAtendimento = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#codeBooking")     // Gets a descendent with id="codeService"
      .text();

    var dataAtendimento = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#dataAtendimento")     // Gets a descendent with id="codeService"
      .text();
    
    var nomeCliente = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#nomeCliente")     // Gets a descendent with id="codeService"
      .text();

    var periodoAtendimento = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#periodoAtendimento")     // Gets a descendent with id="codeService"
      .text();
    
    var agendadoEm = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#agendadoEm")     // Gets a descendent with id="codeService"
      .text();
      
    var statusAtendimento = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#statusAtendimento")     // Gets a descendent with id="codeService"
      .text();
    
    var emailCliente = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#emailCliente")     // Gets a descendent with id="codeService"
      .text();

    var observacaoCliente = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#observacaoCliente")     // Gets a descendent with id="codeService"
      .text();
    
    var avaliacaoCliente = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#avaliacaoCliente")     // Gets a descendent with id="codeService"
      .text();
      
    var observacaoAgendamento = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#observacaoAgendamento")     // Gets a descendent with id="codeService"
      .text();
  
    var observacaoEspecialista = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#observacaoEspecialista")     // Gets a descendent with id="codeService"
      .text();
  
    var observacaoAvaliacaoCliente = $(this)
      .closest("tr")   // Finds the closest row <tr> 
      .find("#observacaoAvaliacaoCliente")     // Gets a descendent with id="codeService"
      .text();

    $('#maisInformacoesDataAtendimento').html(dataAtendimento);
    $('#maisInformacoesNomeCliente').html(nomeCliente);
    $('#maisInformacoesPeriodoAtendimento').html(periodoAtendimento);
    $('#maisInformacoesAgendadoEm').html(agendadoEm);
    $('#maisInformacoesStatusAtendimento').html(statusAtendimento);
    $('#maisInformacoesObservacaoCliente').html(observacaoCliente);
    $('#idRegistro').attr('value', idAtendimento);
    $('#idRegistroObservacao').attr('value', idAtendimento);
    $('#nomeCliente').attr('value', nomeCliente);
    $('#dataAgendada').attr('value', dataAtendimento);
    $('#emailCliente').attr('value', emailCliente);
    $('#observacaoCliente').attr('value', emailCliente);
    $('#maisInformacoesObservacaoAgendamento').html(observacaoAgendamento);
    $('#maisInformacoesObservacaoEspecialista').html(observacaoEspecialista);
    $('#maisInformacoesAvaliacao').html(avaliacaoCliente);
    $('#maisInformacoesObservacaoAvaliacao').html(observacaoAvaliacaoCliente);

    if(statusAtendimento == 'Finalizado' || statusAtendimento == 'Cancelado'){
      $('#formFinalizarCancelar').hide();
    } else {
      $('#formFinalizarCancelar').show();
    }

    $('#modalAvaliacaoAtendimento').modal('show');
    $('#modalMaisInformacoes').modal('show');
  });
});

// Habilitar o modal de Avaliação do Cliente
// através do clique no botão Mostrar Avaliação
$('td #btnMostrarAvaliacao').click(function () {

  var dataAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#dataAtendimento")     // Gets a descendent with id="codeService"
    .text();
  
  var nomeCliente = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#nomeCliente")     // Gets a descendent with id="codeService"
    .text();

  var periodoAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#periodoAtendimento")     // Gets a descendent with id="codeService"
    .text();
  
  var agendadoEm = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#agendadoEm")     // Gets a descendent with id="codeService"
    .text();
    
  var statusAtendimento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#statusAtendimento")     // Gets a descendent with id="codeService"
    .text();

    
  var avaliacaoCliente = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#avaliacaoCliente")     // Gets a descendent with id="codeService"
    .text();
    
  var observacaoAgendamento = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#observacaoAgendamento")     // Gets a descendent with id="codeService"
    .text();

  var observacaoEspecialista = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#observacaoEspecialista")     // Gets a descendent with id="codeService"
    .text();

  var observacaoAvaliacaoCliente = $(this)
    .closest("tr")   // Finds the closest row <tr> 
    .find("#observacaoAvaliacaoCliente")     // Gets a descendent with id="codeService"
    .text();

  $('#maisInformacoesDataAtendimento').html(dataAtendimento);
  $('#maisInformacoesNomeCliente').html(nomeCliente);
  $('#maisInformacoesPeriodoAtendimento').html(periodoAtendimento);
  $('#maisInformacoesAgendadoEm').html(agendadoEm);
  $('#maisInformacoesStatusAtendimento').html(statusAtendimento);
  $('#maisInformacoesObservacaoAgendamento').html(observacaoAgendamento);
  $('#maisInformacoesObservacaoEspecialista').html(observacaoEspecialista);
  $('#maisInformacoesAvaliacao').html(avaliacaoCliente);
  $('#maisInformacoesObservacaoAvaliacao').html(observacaoAvaliacaoCliente);

  $('#modalAvaliacaoAtendimento').modal('show');
});

// Desabilitar os botões de Finalizar e Cancelar 
// o atendimento
$(document).ready(function (){
  $('#btnFinalizarAtendimento').click(function (){
    $('#inputBotaoEnvio').attr('name', 'finalizar-atendimento');
    $('#btnCancelarAgendamento').removeAttr('name');
    $('#btnFinalizarAtendimento .spinner-border').removeAttr("hidden");
    $('#btnFinalizarAtendimento').prop( "disabled", true );
    $('#btnCancelarAgendamento').prop( "disabled", true );
    $('#btnCancelarEnvioModal').prop('disabled', true);
    $('#btnFecharEnvioModal').prop('disabled', true);
    $('#formFinalizarCancelar').submit();
  });

  $('#btnCancelarAgendamento').click(function (){
    $('#inputBotaoEnvio').attr('name', 'cancelar-atendimento');
    $('#btnFinalizarAtendimento').removeAttr('name');
    $('#btnCancelarAgendamento .spinner-border').removeAttr("hidden");
    $('#btnFinalizarAtendimento').prop( "disabled", true );
    $('#btnCancelarAgendamento').prop( "disabled", true );
    $('#btnCancelarEnvioModal').prop('disabled', true);
    $('#btnFecharEnvioModal').prop('disabled', true);
    $('#formFinalizarCancelar').submit();
  });
});
