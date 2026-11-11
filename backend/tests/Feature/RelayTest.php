<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RelayTest extends TestCase
{
    use RefreshDatabase;

    public function test_panel_requires_login(): void
    {
        $this->get('/')->assertRedirect('/login');
        $this->getJson('/estado')->assertUnauthorized();
        $this->postJson('/encender')->assertUnauthorized();
    }

    public function test_device_requires_valid_token(): void
    {
        config(['device.token' => str_repeat('a', 64)]);
        $this->getJson('/api/esp32/config')->assertUnauthorized();
        $this->withToken('incorrect')->postJson('/api/esp32/estado', ['led' => 'on'])->assertUnauthorized();
    }

    public function test_command_and_confirmation_are_separate_and_persisted(): void
    {
        config(['device.token' => str_repeat('a', 64)]);
        $this->actingAs(User::factory()->create());
        $this->postJson('/encender')->assertStatus(202)->assertJson(['led_deseado' => 'on', 'estado' => 'desconocido']);
        $this->withToken(str_repeat('a', 64))->getJson('/api/esp32/config')->assertOk()->assertJson(['led' => 'on']);
        $this->postJson('/api/esp32/estado', ['led' => 'invalid'])->assertUnprocessable();
        $this->postJson('/api/esp32/estado', ['led' => 'on'])->assertOk();
        $this->getJson('/estado')->assertOk()->assertJson(['estado' => 'encendido']);
        $this->assertDatabaseHas('relays', ['id' => 1, 'desired' => 'on', 'reported' => 'on']);
        $this->postJson('/apagar')->assertStatus(202)->assertJson(['led_deseado' => 'off', 'estado' => 'encendido']);
    }

    public function test_user_can_login_and_logout(): void
    {
        User::factory()->create(['name' => 'operador', 'password' => bcrypt('una-clave-larga-segura')]);
        $this->post('/login', ['usuario' => 'operador', 'password' => 'incorrecta'])->assertSessionHasErrors();
        $this->post('/login', ['usuario' => 'operador', 'password' => 'una-clave-larga-segura'])->assertRedirect('/');
        $this->assertAuthenticated();
        $this->post('/logout')->assertRedirect('/login');
        $this->assertGuest();
    }
}
