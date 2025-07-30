<script lang="ts">
  import {enhance} from '$app/forms';
  import {resolver} from '$lib/utilidades/resolver';
  import type {SubmitFunction} from '@sveltejs/kit';
  import {Alert, Button, Input, Label} from 'flowbite-svelte';
  import {EyeSlashSolid, EyeSolid, ExclamationCircleOutline, LockSolid, EnvelopeSolid} from 'flowbite-svelte-icons';

  let password = $state('');
  let error = $state('');
  let errorCode = $state('');
  let visible = $state(false);
  let loading = $state(false);

  const toggleVisibility = () => (visible = !visible);

  const handleSubmit: SubmitFunction = () => {
    loading = true;
    error = '';
    errorCode = '';
    
    return async ({ result }) => {
      loading = false;
      
      if (result.type === 'failure') {
        error = result.data?.message || 'Error al iniciar sesión';
        errorCode = result.data?.error_code || '';
      }
    };
  };
</script>

<div class="min-h-screen flex items-center justify-center bg-blue-50 dark:bg-gray-900 relative">

    <form
            method="post"
            use:enhance={handleSubmit}
            class="w-full max-w-md bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl space-y-6"
    >
        <h1 class="text-2xl font-bold text-center text-blue-700 dark:text-white">Iniciar sesión</h1>

        {#if error}
            <Alert color="red" class="text-sm flex items-center gap-2">
                <ExclamationCircleOutline class="w-4 h-4" />
                <span>{error}</span>
            </Alert>
        {/if}

        <div>
            <Label for="correo">Correo</Label>
            <div class="relative">
                <Input id="correo" name="correo" type="email" placeholder="usuario@ejemplo.com" required>
                    {#snippet left()}
                        <EnvelopeSolid class="w-4 h-4 text-gray-500" />
                    {/snippet}
                </Input>
            </div>
        </div>

        <div>
            <Label for="password">Contraseña</Label>
            <div class="relative">
                <Input
                        id="password"
                        bind:value={password}
                        type={visible ? 'text' : 'password'}
                        name="password"
                        placeholder="••••••••"
                        required
                >
                    {#snippet left()}
                        <LockSolid class="w-4 h-4 text-gray-500" />
                    {/snippet}
                    {#snippet right()}
                        <Button
                                type="button"
                                outline
                                size="xs"
                                class="!p-2"
                                onclick={toggleVisibility}
                        >
                            {#if visible}
                                <EyeSlashSolid/>
                            {:else}
                                <EyeSolid/>
                            {/if}
                        </Button>
                    {/snippet}
                </Input>
            </div>
        </div>

        <Button type="submit" color="blue" class="w-full" disabled={loading}>Entrar</Button>

        <div class="text-center">
            <a href="/recuperar" class="text-sm text-blue-600 hover:underline dark:text-blue-500">
                ¿Olvidaste tu contraseña?
            </a>
        </div>
    </form>
</div>