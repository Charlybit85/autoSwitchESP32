<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('relays', function (Blueprint $table) {
            $table->id();
            $table->string('desired')->default('off');
            $table->string('reported')->nullable();
            $table->timestamp('last_seen_at')->nullable();
            $table->timestamps();
        });
        DB::table('relays')->insert(['id' => 1, 'desired' => 'off', 'created_at' => now(), 'updated_at' => now()]);
    }

    public function down(): void
    {
        Schema::dropIfExists('relays');
    }
};
