<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Relay extends Model
{
    protected $fillable = ['desired', 'reported', 'last_seen_at'];

    protected function casts(): array
    {
        return ['last_seen_at' => 'datetime'];
    }

    public function state(): string
    {
        return match ($this->reported) {
            'on' => 'encendido', 'off' => 'apagado', default => 'desconocido'
        };
    }
}
