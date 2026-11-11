<?php

use App\Http\Controllers\RelayController;
use App\Http\Middleware\DeviceToken;
use Illuminate\Support\Facades\Route;

Route::middleware([DeviceToken::class, 'throttle:120,1'])->prefix('esp32')->group(function () {
    Route::get('/config', [RelayController::class, 'config']);
    Route::post('/estado', [RelayController::class, 'report']);
});
