<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control de Interruptor</title>
    <link rel="stylesheet" href="{{ asset('css/style.css') }}">
<meta name="csrf-token" content="{{ csrf_token() }}">
</head>
<body>
    <main class="panel">
        <h1>Control de Interruptor</h1>
        <div class="estado">
            <span id="indicator" class="indicador desconocido"></span>
            <span id="estadoText">Cargando...</span>
        </div>
        <div class="botones">
            <button id="btn-encender" type="button">Encender</button>
            <button id="btn-apagar" type="button">Apagar</button>
        </div>
        <p id="error" class="error" role="alert" hidden></p>
        <div class="usuario-barra">
            <span>Sesion: <strong>{{ $usuario }}</strong></span>
            <form method="post" action="/logout">@csrf
                <button type="submit" class="btn-salir">Cerrar sesión</button>
            </form>
        </div>
    </main>
    <script src="{{ asset('js/app.js') }}" defer></script>
</body>
</html>