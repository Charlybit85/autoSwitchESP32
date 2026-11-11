<?php

namespace App\Http\Controllers;

use App\Models\Relay;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class RelayController extends Controller
{
    public function state(): JsonResponse
    {
        $relay = Relay::findOrFail(1);

        return response()->json(['ok' => true, 'estado' => $relay->state(), 'led_deseado' => $relay->desired, 'led_reportado' => $relay->reported]);
    }

    public function command(Request $request, ?string $state = null): JsonResponse
    {
        $state ??= $request->validate(['estado' => 'required|in:on,off'])['estado'];
        $relay = Relay::findOrFail(1);
        $relay->update(['desired' => $state]);

        return response()->json(['ok' => true, 'estado' => $relay->state(), 'led_deseado' => $state], 202);
    }

    public function config(): JsonResponse
    {
        return response()->json(['led' => Relay::findOrFail(1)->desired]);
    }

    public function report(Request $request): JsonResponse
    {
        $data = $request->validate(['led' => 'required|in:on,off']);
        Relay::findOrFail(1)->update(['reported' => $data['led'], 'last_seen_at' => now()]);

        return response()->json(['ok' => true]);
    }
}
