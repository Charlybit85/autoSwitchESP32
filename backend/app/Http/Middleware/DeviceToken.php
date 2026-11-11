<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class DeviceToken
{
    public function handle(Request $request, Closure $next): Response
    {
        $token = config('device.token');
        if (! is_string($token) || strlen($token) < 32 || ! hash_equals($token, $request->bearerToken() ?? '')) {
            return response()->json(['error' => 'Dispositivo no autorizado.'], 401);
        }

        return $next($request);
    }
}
