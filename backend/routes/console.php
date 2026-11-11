<?php

use App\Models\User;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Hash;

Artisan::command('app:create-user {name}', function () {
    $name = $this->argument('name');
    if (User::where('name', $name)->exists()) {
        $this->error('El usuario ya existe.');

        return 1;
    }
    $password = $this->secret('Contraseña (mínimo 12 caracteres)');
    if (strlen($password ?? '') < 12 || $password !== $this->secret('Confirmar contraseña')) {
        $this->error('Contraseña inválida o no coincide.');

        return 1;
    }
    User::create(['name' => $name, 'email' => bin2hex(random_bytes(16)).'@local.invalid', 'password' => Hash::make($password)]);
    $this->info('Usuario creado.');
});
