<script lang="ts">
	import type { AudioEntry } from '../player/types.js';
	import type { Category } from '../category-themes.js';
	import { getAudioDescription } from '../utils/spsq-parser.js';
	import { getCategoryTheme } from '../category-themes.js';
	import { X } from '@lucide/svelte';
	import { defaultArtwork } from '../player/constants.js';

	let {
		show = false,
		audio = null,
		onclose = null
	}: {
		show: boolean;
		audio: (AudioEntry & { artwork: string }) | null;
		onclose: (() => void) | null;
	} = $props();

	let description = $state<string[]>([]);
	let loading = $state(false);
	let imgError = $state(false);

	let categoryTheme = $derived(audio ? getCategoryTheme(audio.category as Category) : null);

	// RGB values per category color name, for inline gradient usage
	const categoryRgb: Record<string, string> = {
		rose: '244, 63, 94',
		teal: '20, 184, 166',
		amber: '245, 158, 11',
		neutral: '115, 115, 115'
	};

	let categoryColorName = $derived.by(() => {
		if (!categoryTheme) return null;
		const m = categoryTheme.bgSubtleClass.match(/bg-(\w+)-500/);
		return m ? m[1] : null;
	});

	let categoryRgbValue = $derived(
		categoryColorName ? (categoryRgb[categoryColorName] ?? null) : null
	);

	$effect(() => {
		if (show && audio?.path) {
			loading = true;
			imgError = false;
			getAudioDescription(audio.path)
				.then((lines) => {
					description = lines;
					loading = false;
				})
				.catch(() => {
					description = [];
					loading = false;
				});
		} else {
			description = [];
			imgError = false;
		}
	});

	function handleClose() {
		if (onclose) onclose();
	}

	function handleOverlayClick(e: MouseEvent) {
		if (e.target === e.currentTarget) handleClose();
	}

	function handleOverlayKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') handleClose();
	}

	function useFallback(event: Event) {
		imgError = true;
		const img = event.currentTarget as HTMLImageElement;
		if (!img.src.endsWith(defaultArtwork)) img.src = defaultArtwork;
	}

	// --- Swipe-to-dismiss ---
	const DISMISS_THRESHOLD_PX = 80;
	const DISMISS_VELOCITY = 0.5; // px/ms

	let dragY = $state(0);
	let dragging = $state(false);
	let startY = 0;
	let startTime = 0;

	function onDragStart(e: PointerEvent) {
		// Only handle touch-like input (touch or stylus) on mobile, or any pointer on the handle itself
		dragging = true;
		startY = e.clientY;
		startTime = e.timeStamp;
		dragY = 0;
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
	}

	function onDragMove(e: PointerEvent) {
		if (!dragging) return;
		const delta = e.clientY - startY;
		// Only allow downward drag
		dragY = Math.max(0, delta);
	}

	function onDragEnd(e: PointerEvent) {
		if (!dragging) return;
		dragging = false;

		const elapsed = e.timeStamp - startTime;
		const velocity = elapsed > 0 ? dragY / elapsed : 0;

		if (dragY >= DISMISS_THRESHOLD_PX || velocity >= DISMISS_VELOCITY) {
			// Animate out, close, then reset so the next open starts clean
			dragY = window.innerHeight;
			setTimeout(() => {
				handleClose();
				dragY = 0;
			}, 220);
		} else {
			// Snap back
			dragY = 0;
		}
	}
</script>

{#if show && audio}
	<!-- Overlay -->
	<div
		class="fixed inset-0 z-50 flex items-end justify-center lg:items-center"
		role="dialog"
		aria-modal="true"
		aria-label={audio.name}
		tabindex="-1"
		onclick={handleOverlayClick}
		onkeydown={handleOverlayKeydown}
	>
		<!-- Backdrop -->
		<div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

		<!-- Sheet (mobile) / Card (desktop) -->
		<div
			class="relative z-10 w-full overflow-hidden rounded-t-[28px] border border-[var(--line)] bg-[var(--panel-strong)] shadow-[0_-8px_48px_rgba(0,0,0,0.22)] lg:mx-6 lg:max-w-2xl lg:rounded-[32px] lg:shadow-[var(--shadow)]"
			style="transform: translateY({dragY}px); transition: {dragging ? 'none' : 'transform 0.22s cubic-bezier(0.32,0.72,0,1)'};"
		>
			<!-- Category color wash -->
			{#if categoryRgbValue}
				<div
					class="pointer-events-none absolute inset-x-0 top-0 h-56 rounded-t-[28px] lg:rounded-t-[32px]"
					style="background: linear-gradient(180deg, rgba({categoryRgbValue}, 0.18) 0%, transparent 100%);"
				></div>
			{/if}

			<!-- Drag handle (mobile only) -->
			<div
				class="flex touch-none justify-center pt-3 pb-1 lg:hidden"
				role="presentation"
				onpointerdown={onDragStart}
				onpointermove={onDragMove}
				onpointerup={onDragEnd}
				onpointercancel={onDragEnd}
			>
				<div class="h-1 w-10 rounded-full bg-[var(--line-strong)]"></div>
			</div>

			<!-- Close button -->
			<button
				class="absolute top-4 right-4 inline-flex h-9 w-9 cursor-pointer items-center justify-center rounded-full border border-[var(--line)] bg-[var(--panel-strong)] text-[var(--muted)] transition-all duration-150 hover:border-[var(--line-strong)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)] active:scale-90"
				onclick={handleClose}
				aria-label="Close"
			>
				<X size={16} />
			</button>

			<!-- ── MOBILE layout ── -->
			<div class="px-5 pt-4 pb-8 lg:hidden">
				<div class="flex items-start gap-4">
					<div class="relative shrink-0">
						{#if categoryRgbValue}
							<div class="absolute inset-0 rounded-2xl blur-[14px]" style="background: rgba({categoryRgbValue}, 0.35);"></div>
						{/if}
						<img src={audio.artwork} alt="" class="relative h-[88px] w-[88px] rounded-2xl border border-[var(--line-strong)] object-cover shadow-md" onerror={useFallback} />
					</div>
					<div class="grid min-w-0 flex-1 gap-1 pt-1">
						<h2 class="m-0 text-[1.05rem] leading-snug font-[740] tracking-[-0.03em] text-[var(--text)]">{audio.name}</h2>
						{#if categoryRgbValue}
							<span class="inline-flex w-fit items-center rounded-full px-2.5 py-0.5 text-[0.7rem] font-[600] tracking-[0.1em] uppercase" style="background: rgba({categoryRgbValue}, 0.15); color: rgba({categoryRgbValue}, 1);">{audio.category}</span>
						{:else}
							<span class="text-[0.75rem] font-[500] tracking-[0.1em] text-[var(--muted)] uppercase">{audio.category}</span>
						{/if}
					</div>
				</div>
				<div class="my-5 h-px bg-[var(--line)]"></div>
				{#if loading}
					<div class="flex flex-col gap-2.5 py-4">
						<div class="h-2 w-full animate-pulse rounded-full bg-[var(--line-strong)]"></div>
						<div class="h-2 w-4/5 animate-pulse rounded-full bg-[var(--line-strong)]"></div>
						<div class="h-2 w-2/3 animate-pulse rounded-full bg-[var(--line-strong)]"></div>
					</div>
				{:else if description.length > 0}
					<div class="scrollbar-none max-h-[180px] overflow-y-auto">
						<p class="m-0 text-[0.88rem] leading-relaxed whitespace-pre-wrap text-[var(--muted)]">{description.join('\n')}</p>
					</div>
				{:else}
					<p class="m-0 text-[0.85rem] text-[var(--muted)] italic">No description available.</p>
				{/if}
				<div class="mt-6">
					<button class="w-full cursor-pointer rounded-2xl border border-transparent bg-[var(--accent)] py-3 text-[0.92rem] font-[660] text-[#fffaf1] shadow-[0_2px_12px_rgba(177,77,42,0.35)] transition-all duration-150 hover:-translate-y-px hover:bg-[var(--accent-strong)] active:scale-[0.98]" onclick={handleClose}>Got it</button>
				</div>
			</div>

			<!-- ── DESKTOP layout ── -->
			<div class="hidden lg:grid lg:grid-cols-[220px_1fr] lg:gap-0">

				<!-- Left column: artwork + meta -->
				<div class="relative flex flex-col items-center px-7 py-8 after:absolute after:right-0 after:top-6 after:bottom-6 after:w-px after:bg-[var(--line)]">
					{#if categoryRgbValue}
						<div class="absolute inset-0 rounded-l-[32px]" style="background: linear-gradient(135deg, rgba({categoryRgbValue}, 0.12) 0%, transparent 70%);"></div>
					{/if}
					<div class="relative mb-5 shrink-0">
						{#if categoryRgbValue}
							<div class="absolute inset-0 rounded-3xl blur-[18px]" style="background: rgba({categoryRgbValue}, 0.4);"></div>
						{/if}
						<img
							src={audio.artwork}
							alt=""
							class="relative h-[148px] w-[148px] rounded-3xl border border-[var(--line-strong)] object-cover shadow-lg"
							onerror={useFallback}
						/>
					</div>

					<div class="relative w-full text-center">
						<h2 class="m-0 mb-2 text-[1.05rem] font-[760] leading-snug tracking-[-0.03em] text-[var(--text)]">
							{audio.name}
						</h2>
						{#if categoryRgbValue}
							<span
								class="inline-flex items-center rounded-full px-3 py-1 text-[0.68rem] font-[640] tracking-[0.12em] uppercase"
								style="background: rgba({categoryRgbValue}, 0.15); color: rgba({categoryRgbValue}, 1);"
							>
								{audio.category}
							</span>
						{:else}
							<span class="text-[0.72rem] font-[500] tracking-[0.1em] text-[var(--muted)] uppercase">{audio.category}</span>
						{/if}
					</div>
				</div>

				<!-- Right column: description + action -->
				<div class="flex flex-col px-7 py-8">
					<p class="mb-4 text-[0.68rem] font-[660] uppercase tracking-[0.13em] text-[var(--muted)]">About this audio</p>

					{#if loading}
						<div class="flex flex-1 flex-col gap-2.5 py-2">
							<div class="h-2 w-full animate-pulse rounded-full bg-[var(--line-strong)]"></div>
							<div class="h-2 w-[92%] animate-pulse rounded-full bg-[var(--line-strong)]"></div>
							<div class="h-2 w-4/5 animate-pulse rounded-full bg-[var(--line-strong)]"></div>
							<div class="h-2 w-3/4 animate-pulse rounded-full bg-[var(--line-strong)]"></div>
						</div>
					{:else if description.length > 0}
						<div class="scrollbar-none flex-1 overflow-y-auto">
							<p class="m-0 text-[0.9rem] leading-relaxed whitespace-pre-wrap text-[var(--muted)]">
								{description.join('\n')}
							</p>
						</div>
					{:else}
						<p class="m-0 flex-1 text-[0.88rem] italic text-[var(--muted)]">No description available.</p>
					{/if}

					<div class="mt-6 flex justify-end">
						<button
							class="cursor-pointer rounded-2xl border border-transparent bg-[var(--accent)] px-8 py-2.5 text-[0.9rem] font-[660] text-[#fffaf1] shadow-[0_2px_12px_rgba(177,77,42,0.32)] transition-all duration-150 hover:-translate-y-px hover:bg-[var(--accent-strong)] hover:shadow-[0_4px_16px_rgba(177,77,42,0.42)] active:scale-[0.98]"
							onclick={handleClose}
						>
							Got it
						</button>
					</div>
				</div>

			</div>
		</div>
	</div>
{/if}
