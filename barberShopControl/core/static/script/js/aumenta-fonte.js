var $btnAumentar = $("#btnAumentar");
var $btnDiminuir = $("#btnDiminuir");
var $elemento = $("body p, h2");

function obterTamanhoFonte() {
  return parseFloat($elemento.css("font-size"));
}

$btnAumentar.on("click", function () {
  $elemento.css("font-size", obterTamanhoFonte() + 1);
});

$btnDiminuir.on("click", function () {
  $elemento.css("font-size", obterTamanhoFonte() - 1);
});
