<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function login(Request $request): RedirectResponse
    {
        $data = $request->validate(['usuario' => 'required|string|max:255', 'password' => 'required|string|max:1024']);
        if (! Auth::attempt(['name' => $data['usuario'], 'password' => $data['password']])) {
            return back()->withErrors(['usuario' => 'Credenciales inválidas.'])->onlyInput('usuario');
        }
        $request->session()->regenerate();

        return redirect()->intended('/');
    }

    public function logout(Request $request): RedirectResponse
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/login');
    }
}
