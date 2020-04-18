function pattern() {
    var display = $( window ).width()
    
    if (display <= 575){
        $("img").attr("src", "/static/img/logo-branco.png");
        $('.login-wrapper-footer-text').html('Sem conta? Cadastre-se aqui');
    };
}