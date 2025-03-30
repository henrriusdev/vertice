<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import {
		Sidebar,
		SidebarGroup,
		SidebarItem,
		SidebarWrapper,
		SidebarDropdownWrapper,
		SidebarDropdownItem,
		Button,
		Navbar,
		NavBrand,
		Avatar,
		Breadcrumb,
		BreadcrumbItem,
		Alert,
		Tooltip
	} from 'flowbite-svelte';
	import {
		HomeOutline,
		ChartPieOutline,
		CogOutline,
		UserCircleOutline,
		UsersOutline,
		FileOutline,
		ShieldCheckOutline,
		ChevronDownOutline,
		BarsOutline,
		ChevronRightOutline,
		ChevronLeftOutline,

		UsersGroupOutline,

		ListOutline,

		UserHeadsetOutline,

		BuildingOutline,

		BookOpenOutline





	} from 'flowbite-svelte-icons';

	// Obtener los datos del usuario desde los datos proporcionados por +layout.server.ts
	export let data;

	// Estado para controlar si el sidebar está abierto o cerrado
	let sidebarOpen = true;

	// Estado para mostrar alertas
	let showAlert = false;
	let alertMessage = '';
	let alertColor:
		| 'red'
		| 'form'
		| 'none'
		| 'gray'
		| 'yellow'
		| 'green'
		| 'indigo'
		| 'purple'
		| 'pink'
		| 'blue'
		| 'light'
		| 'dark'
		| 'default'
		| 'dropdown'
		| 'navbar'
		| 'navbarUl'
		| 'primary'
		| 'orange'
		| undefined = 'red';

	// Función para alternar el estado del sidebar
	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}

	// Elementos de navegación con roles permitidos
	const elementosNav = [
		{
			titulo: 'Inicio',
			icono: HomeOutline,
			href: '/'+data.rol,
			roles: [] // Todos pueden ver el inicio
		},
		{
      titulo: "Docentes",
      icono: UsersOutline,
      href: "/superusuario/docentes",
      roles: ["superusuario"]
    },
    {
      titulo: "Estudiantes",
      icono: UsersGroupOutline,
      href: "/superusuario/estudiantes",
      roles: ["superusuario"]
    },
    {
      titulo: "Asignaturas",
      icono: ListOutline,
      href: "/superusuario/asignaturas",
      roles: ["superusuario"]
    },
    {
      titulo: "Coordinadores",
      icono: UserHeadsetOutline,
      href: "/superusuario/coordinadores",
      roles: ["superusuario"]
    },
    {
      titulo: "Carreras",
      icono: BuildingOutline,
      href: "/superusuario/carreras",
      roles: ["superusuario"]
    },
    {
      titulo: "Movimientos",
      icono: BookOpenOutline,
      href: "/superusuario/movimientos",
      roles: ["superusuario"]
    }
	];

	// Función para generar las migas de pan basadas en la URL
	$: rutaActual = $page.url.pathname;

	$: migasDePan = generarMigasDePan(rutaActual);

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
	$: if (data && data.nombre) {
		const rutaActual = $page.url.pathname;
		const rutaEncontrada = elementosNav.find((item) => item.href === rutaActual);

		if (rutaEncontrada && !hasAccess(rutaEncontrada.roles, data.rol)) {
			showAlert = true;
			alertMessage = 'No tienes permiso para acceder a esta página';
			alertColor = 'red';

			// Redirigir al inicio después de mostrar la alerta
			setTimeout(() => {
				goto('/');
			}, 2000);
		}
	}

	// Función para cerrar sesión (redirige a la ruta de logout)
	function cerrarSesion() {
		goto('/logout');
	}
</script>

<div class="flex w-full h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
	<!-- Sidebar -->
	<div class="relative">
		<Sidebar
			activeUrl={rutaActual}
			class="fixed left-0 top-0 z-40 h-screen transition-all duration-300 {sidebarOpen
				? 'w-64'
				: 'w-16'} border-r border-gray-200 dark:border-gray-700"
		>
			<SidebarWrapper class="h-full px-3 py-4 overflow-y-auto">
				<div class="flex items-center mb-5 {sidebarOpen ? 'pl-2.5' : 'justify-center !pl-[-2px]'}">
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
									<SidebarItem href={item.href} label={item.titulo} >
										<svelte:fragment slot="icon">
											<svelte:component this={item.icono} class="w-5 h-5" />
										</svelte:fragment>
									</SidebarItem>
								{:else}
									<div class="mb-2">
											<SidebarItem href={item.href} spanClass="!px-2 !py-1" title={item.titulo}>
												<svelte:fragment slot="icon">
													<svelte:component this={item.icono} class="w-5 h-5" />
												</svelte:fragment>
											</SidebarItem>
									</div>
								{/if}
							{/if}
						{/each}
					</SidebarGroup>

					<!-- Perfil de usuario en la parte inferior -->
					<div
						class="absolute bottom-0 left-0 w-full p-4 border-t border-gray-200 dark:border-gray-700"
					>
						{#if sidebarOpen}
							<SidebarDropdownWrapper
								label={data.nombre}
								class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
							>
								<svelte:fragment slot="icon">
									<Avatar src="/placeholder.svg?height=32&width=32" class="mr-3" />
								</svelte:fragment>
								<svelte:fragment slot="caret">
									<ChevronDownOutline class="w-4 h-4" />
								</svelte:fragment>
								<div class="px-4 py-2 text-sm text-gray-900 dark:text-white">
									<div class="font-medium truncate">{data.nombre}</div>
									<div class="truncate text-gray-500">Rol: {data.rol}</div>
								</div>
								<SidebarDropdownItem href="/perfil">
									<UserCircleOutline class="w-5 h-5 mr-2" />
									Mi Perfil
								</SidebarDropdownItem>
								<SidebarDropdownItem href="/configuracion">
									<CogOutline class="w-5 h-5 mr-2" />
									Configuración
								</SidebarDropdownItem>
								<SidebarDropdownItem on:click={cerrarSesion}>
									<ShieldCheckOutline class="w-5 h-5 mr-2" />
									Cerrar Sesión
								</SidebarDropdownItem>
							</SidebarDropdownWrapper>
						{:else}
							<Tooltip content="Perfil de Usuario" placement="right">
								<Button class="w-full p-2 flex justify-center" color="light">
									<Avatar src="/placeholder.svg?height=32&width=32" size="xs" />
								</Button>
							</Tooltip>
						{/if}
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
	</div>

	<!-- Contenido principal -->
	<div
		class="flex flex-col flex-1 {sidebarOpen ? 'md:ml-64' : 'md:ml-16'} transition-all duration-300"
	>
		<!-- Barra superior -->
		<Navbar class="border-b border-gray-200 dark:border-gray-700">
			<div class="flex items-center">
				<Button color="light" class="mr-2 md:mr-4 !p-2" size="xs" on:click={toggleSidebar}>
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
			<NavBrand href="/">
				<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white md:hidden">
					Vertice
				</span>
			</NavBrand>
		</Navbar>

		<!-- Alertas -->
		{#if showAlert}
			<Alert color={alertColor} dismissable bind:open={showAlert} class="mt-2 mx-4">
				{alertMessage}
			</Alert>
		{/if}

		<!-- Contenido de la página -->
		<main class="flex-1 p-4 {sidebarOpen ?'w-[calc(100%-310px)]' : 'w-[calc(100%-110px)]'} overflow-y-auto h-full">
			<slot />
		</main>
	</div>
</div>
