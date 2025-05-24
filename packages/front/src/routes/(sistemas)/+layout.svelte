<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { addToast } from '$lib';
	import {
		Avatar,
		Breadcrumb,
		BreadcrumbItem,
		Button,
		Dropdown,
		DropdownDivider,
		DropdownItem,
		Navbar,
		Sidebar,
		SidebarGroup,
		SidebarItem,
		SidebarWrapper
	} from 'flowbite-svelte';
	import {
		BookOpenOutline,
		BuildingOutline,
		CalendarMonthOutline,
		ChalkboardUserOutline,
		ChevronLeftOutline,
		ChevronRightOutline,
		CogOutline,
		HomeOutline,
		ListOutline,
		ReceiptOutline,
		ShieldCheckOutline,
		UserCircleOutline,
		UserHeadsetOutline,
		UsersGroupOutline,
		UsersOutline
	} from 'flowbite-svelte-icons';
	import type { LayoutData } from './$types';

	// Obtener los datos del usuario desde los datos proporcionados por +layout.server.ts
	let { data, children } = $props<{ data: LayoutData }>();

	// Estado para controlar si el sidebar está abierto o cerrado
	let sidebarOpen = $state(true);

	// Estado para mostrar alertas
	let userDropdownOpen = $state(false);

	// Función para alternar el estado del sidebar
	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}

	function toggleUserDropdown() {
		userDropdownOpen = !userDropdownOpen;
	}

	const elementosNav = [
		{
			titulo: 'Inicio',
			icono: HomeOutline,
			href: '/' + data.rol,
			roles: [] // Todos pueden ver el inicio
		},
		{
			titulo: 'Docentes',
			icono: UsersOutline,
			href: '/docentes',
			roles: ['superusuario', 'coordinador', 'control']
		},
		{
			titulo: 'Estudiantes',
			icono: UsersGroupOutline,
			href: '/estudiantes',
			roles: ['superusuario', 'caja', 'coordinador']
		},
		{
			titulo: 'Materias',
			icono: ListOutline,
			href: '/materias',
			roles: ['coordinador', 'control']
		},
		{
			titulo: 'Usuarios',
			icono: UsersOutline,
			href: '/superusuario/usuarios',
			roles: ['superusuario']
		},
		{
			titulo: 'Coordinadores',
			icono: UserHeadsetOutline,
			href: '/superusuario/coordinadores',
			roles: ['superusuario']
		},
		{
			titulo: 'Carreras',
			icono: BuildingOutline,
			href: '/superusuario/carreras',
			roles: ['superusuario']
		},
		{
			titulo: 'Trazabilidad',
			icono: BookOpenOutline,
			href: '/superusuario/trazabilidad',
			roles: ['superusuario']
		},
		{
			titulo: 'Pagos',
			icono: ReceiptOutline,
			href: '/caja/pagos',
			roles: ['caja']
		},
		{
			titulo: 'Configuración',
			icono: CogOutline,
			href: '/configuracion',
			roles: ['superusuario', 'coordinador']
		},
		{
			titulo: 'Horario',
			icono: CalendarMonthOutline,
			href: '/estudiante/horario',
			roles: ['estudiante']
		},
		{
			titulo: 'Histórico de notas',
			icono: ShieldCheckOutline,
			href: '/estudiante/notas',
			roles: ['estudiante']
		},
		{
			titulo: 'Cursando',
			icono: BookOpenOutline,
			href: '/estudiante/materias',
			roles: ['estudiante']
		},
		{
			titulo: 'Peticiones',
			icono: ChalkboardUserOutline,
			href: '/peticiones',
			roles: ['docente', 'control']
		}
	];

	// Función para generar las migas de pan basadas en la URL
	let rutaActual = $derived(page.url.pathname);
	let migasDePan = $derived(generarMigasDePan(rutaActual));

	function generarMigasDePan(ruta: string) {
		// Ignorar la primera barra y dividir la ruta
		const segmentos = ruta.split('/').filter(Boolean);

		if (segmentos.length === 0) {
			return [{ titulo: 'Inicio', href: '/', actual: true }];
		}

		// Crear las migas de pan
		const migas: { titulo: string; href: string; actual: boolean }[] = [];

		let rutaAcumulada = '';
		segmentos.forEach((segmento, index) => {
			rutaAcumulada += `/${segmento}`;

			// Convertir el segmento a un formato más legible
			const titulo = segmento.charAt(0).toUpperCase() + segmento.slice(1);

			migas.push({
				titulo,
				href: rutaAcumulada,
				actual: index === segmentos.length - 1
			});
		});

		return migas;
	}

	// Mapeo de rutas a nombres más amigables en español
	const mapeoRutas: { [key: string]: string } = {
		'/': 'Inicio',
		'/panel': 'Panel de Control',
		'/usuarios': 'Gestión de Usuarios',
		'/documentos': 'Documentos',
		'/configuracion': 'Configuración'
	};

	// Verificar si el usuario tiene acceso a una ruta específica
	function hasAccess(requiredRoles: string[], userRole: string) {
		if (!requiredRoles || requiredRoles.length === 0) {
			return true; // Si no hay roles requeridos, todos tienen acceso
		}

		return requiredRoles.includes(userRole);
	}

	// Verificar acceso a la ruta actual
	$effect(() => {
		if (data && data.nombre) {
			const rutaActual = page.url.pathname;
			const rutaEncontrada = elementosNav.find((item) => item.href === rutaActual);

			if (rutaEncontrada && !hasAccess(rutaEncontrada.roles, data.rol)) {
				// mostrar toast de acceso denegado
				addToast({
					type: 'error',
					message: 'Acceso denegado a esta sección.'
				});

				// Redirigir al inicio después de mostrar la alerta
				setTimeout(() => {
					goto('/');
				}, 2000);
			}
		}
	});

	// Función para cerrar sesión (redirige a la ruta de logout)
	function cerrarSesion() {
		goto('/logout');
	}
</script>

<!-- Main layout container with fixed height and no overflow -->
<div class="flex w-full h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
	<!-- Sidebar - fixed height with its own scrollbar -->
	<Sidebar
		activeUrl={rutaActual}
		class="relative z-40 h-screen transition-all duration-300 {sidebarOpen
			? 'w-72 min-w-72'
			: 'w-16 min-w-16'} border-r border-gray-200 dark:border-gray-700"
	>
		<SidebarWrapper class="h-full py-4 overflow-y-auto">
			<div class="flex items-center mb-5 pl-2.5 justify-start">
				{#if sidebarOpen}
					<span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
						>Vertice</span
					>
				{:else}
					<span class="text-xl font-semibold dark:text-white">V</span>
				{/if}
			</div>

			{#if data && data.nombre}
				<SidebarGroup>
					{#each elementosNav as item}
						{#if hasAccess(item.roles, data.rol)}
							{#if sidebarOpen}
								<SidebarItem href={item.href} label={item.titulo}>
									{#snippet icon()}
										<item.icono class="w-5 h-5" />
									{/snippet}
								</SidebarItem>
							{:else}
								<div class="mb-2">
									<SidebarItem href={item.href} title={item.titulo}>
										{#snippet icon()}
											<item.icono class="w-5 h-5" />
										{/snippet}
									</SidebarItem>
								</div>
							{/if}
						{/if}
					{/each}
				</SidebarGroup>

				<!-- Perfil de usuario en la parte inferior -->
				<!-- User profile at the bottom - now with popup -->
				<div
					class="absolute bottom-0 left-0 w-full p-4 border-t border-gray-200 dark:border-gray-700"
				>
					<!-- User profile button that triggers the dropdown -->
					<div class="relative">
						<Button
							color="alternative"
							class="flex items-center w-full gap-2 text-sm "
							onclick={toggleUserDropdown}
						>
							<Avatar src={`https://unavatar.io/${data.correo}`} class="mr-3" />
							{#if sidebarOpen}
								<div class="flex-1 text-left">
									<span class="font-medium truncate">{data.nombre}</span>
								</div>
							{/if}
						</Button>

						<!-- Dropdown menu that appears as a popup -->
						<Dropdown
							bind:isOpen={userDropdownOpen}
							class="z-50 {sidebarOpen ? 'left-0' : 'left-16'} bottom-14 w-56"
							onclick={() => (userDropdownOpen = false)}
						>
							<div class="px-4 py-3 text-sm text-gray-900 dark:text-white">
								<div class="font-medium">{data.nombre}</div>
								<div class="truncate text-gray-500">Rol: {data.rol}</div>
							</div>
							<DropdownDivider />
							<DropdownItem href="/perfil">
								<div class="flex items-center">
									<UserCircleOutline class="w-5 h-5 mr-2" />
									Mi Perfil
								</div>
							</DropdownItem>
							<DropdownItem href="/configuracion">
								<div class="flex items-center">
									<CogOutline class="w-5 h-5 mr-2" />
									Configuración
								</div>
							</DropdownItem>
							<DropdownDivider />
							<DropdownItem onclick={cerrarSesion}>
								<div class="flex items-center">
									<ShieldCheckOutline class="w-5 h-5 mr-2" />
									Cerrar Sesión
								</div>
							</DropdownItem>
						</Dropdown>
					</div>
				</div>
			{:else}
				<!-- Si no está autenticado, no mostrar nada en el sidebar -->
				<div class="p-4 text-center text-gray-500">
					{#if sidebarOpen}
						No has iniciado sesión
					{:else}
						<span>!</span>
					{/if}
				</div>
			{/if}
		</SidebarWrapper>
	</Sidebar>

	<!-- Content area - flex column with fixed height -->
	<div class="flex flex-col flex-1 h-screen overflow-hidden">
		<!-- Navbar - fixed at top -->
		<Navbar fluid class="w-full border-b border-gray-200 dark:border-gray-700 shrink-0">
			<div class="flex items-center justify-start">
				<Button color="light" class="mr-2 md:mr-4 !p-2" size="xs" onclick={toggleSidebar}>
					{#if sidebarOpen}
						<ChevronLeftOutline class="w-5 h-5" />
					{:else}
						<ChevronRightOutline class="w-5 h-5" />
					{/if}
				</Button>
				<Breadcrumb aria-label="Migas de pan" class="hidden md:flex">
					{#each migasDePan as miga, index}
						<BreadcrumbItem href={miga.href} home={index === 0}>
							{mapeoRutas[miga.href] || miga.titulo}
						</BreadcrumbItem>
					{/each}
				</Breadcrumb>
			</div>
		</Navbar>

		<!-- Main content - only this should scroll vertically -->
		<main class="flex-1 overflow-y-auto p-6 w-full">
			{@render children()}
		</main>
	</div>
</div>

<style>
	:global(.absolute.bottom-0 li::marker) {
		content: none;
	}

	:global(input + div.flex.absolute) {
		padding: 0 !important;
	}
</style>
