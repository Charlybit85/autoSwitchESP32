<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\RelayController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::middleware('guest')->group(function () {
    Route::view('/login', 'login')->name('login');
    Route::get('/templates/login.html', fn () => redirect('/login'));
    Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:5,1');
});
Route::middleware('auth')->group(function () {
    Route::get('/', fn () => view('dashboard', ['usuario' => auth()->user()->name]));
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/estado', [RelayController::class, 'state']);
    Route::get('/api/led', [RelayController::class, 'state']);
    Route::post('/api/led', [RelayController::class, 'command'])->middleware('throttle:60,1');
    Route::post('/encender', fn (Request $r) => (new RelayController)->command($r, 'on'))->middleware('throttle:60,1');
    Route::post('/apagar', fn (Request $r) => (new RelayController)->command($r, 'off'))->middleware('throttle:60,1');
});
