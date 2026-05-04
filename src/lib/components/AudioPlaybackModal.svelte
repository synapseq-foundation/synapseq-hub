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
		class="fixed inset-0 z-50 flex items-end justify-center sm:items-center"
		role="dialog"
		aria-modal="true"
		aria-label={audio.name}
		tabindex="-1"
		onclick={handleOverlayClick}
		onkeydown={handleOverlayKeydown}
	>
		<!-- Backdrop -->
		<div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

		<!-- Sheet / Card -->
		<div
			class="relative z-10 w-full overflow-hidden rounded-t-[28px] border border-[var(--line)] bg-[var(--panel-strong)] shadow-[0_-8px_48px_rgba(0,0,0,0.22)] sm:mx-4 sm:max-w-sm sm:rounded-[28px] sm:shadow-[var(--shadow)]"
			style="transform: translateY({dragY}px); transition: {dragging ? 'none' : 'transform 0.22s cubic-bezier(0.32,0.72,0,1)'};"
		>
			<!-- Category color wash at top -->
			{#if categoryRgbValue}
				<div
					class="pointer-events-none absolute inset-x-0 top-0 h-48 rounded-t-[28px]"
					style="background: linear-gradient(180deg, rgba({categoryRgbValue}, 0.18) 0%, transparent 100%);"
				></div>
			{/if}

			<!-- Drag handle (mobile) — pointer events anchored here -->
			<div
				class="flex touch-none justify-center pt-3 pb-1 sm:hidden"
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

			<!-- Content -->
			<div class="px-5 pt-4 pb-8 sm:px-6 sm:pt-5 sm:pb-8">
				<!-- Artwork + meta -->
				<div class="flex items-start gap-4">
					<!-- Artwork -->
					<div class="relative shrink-0">
						{#if categoryRgbValue}
							<div
								class="absolute inset-0 rounded-2xl blur-[14px]"
								style="background: rgba({categoryRgbValue}, 0.35);"
							></div>
						{/if}
						<img
							src={audio.artwork}
							alt=""
							class="relative h-[88px] w-[88px] rounded-2xl border border-[var(--line-strong)] object-cover shadow-md sm:h-24 sm:w-24"
							onerror={useFallback}
						/>
					</div>

					<!-- Name, category, author -->
					<div class="grid min-w-0 flex-1 gap-1 pt-1">
						<h2
							class="m-0 text-[1.05rem] leading-snug font-[740] tracking-[-0.03em] text-[var(--text)] sm:text-[1.1rem]"
						>
							{audio.name}
						</h2>
						{#if categoryRgbValue}
							<span
								class="inline-flex w-fit items-center rounded-full px-2.5 py-0.5 text-[0.7rem] font-[600] tracking-[0.1em] uppercase"
								style="background: rgba({categoryRgbValue}, 0.15); color: rgba({categoryRgbValue}, 1);"
							>
								{audio.category}
							</span>
						{:else}
							<span
								class="text-[0.75rem] font-[500] tracking-[0.1em] text-[var(--muted)] uppercase"
							>
								{audio.category}
							</span>
						{/if}
					</div>
				</div>

				<!-- Divider -->
				<div class="my-5 h-px bg-[var(--line)]"></div>

				<!-- Description -->
				{#if loading}
					<div class="flex items-center gap-2.5 py-4">
						<div class="h-2 flex-1 animate-pulse rounded-full bg-[var(--line-strong)]"></div>
						<div class="h-2 w-2/3 animate-pulse rounded-full bg-[var(--line-strong)]"></div>
					</div>
				{:else if description.length > 0}
					<div class="scrollbar-none max-h-[180px] overflow-y-auto sm:max-h-[220px]">
						<p
							class="m-0 text-[0.88rem] leading-relaxed whitespace-pre-wrap text-[var(--muted)] sm:text-[0.9rem]"
						>
							{description.join('\n')}
						</p>
					</div>
				{:else}
					<p class="m-0 text-[0.85rem] text-[var(--muted)] italic">No description available.</p>
				{/if}

				<!-- Footer button -->
				<div class="mt-6">
					<button
						class="w-full cursor-pointer rounded-2xl border border-transparent bg-[var(--accent)] py-3 text-[0.92rem] font-[660] text-[#fffaf1] shadow-[0_2px_12px_rgba(177,77,42,0.35)] transition-all duration-150 hover:-translate-y-px hover:bg-[var(--accent-strong)] hover:shadow-[0_4px_16px_rgba(177,77,42,0.45)] active:scale-[0.98]"
						onclick={handleClose}
					>
						Got it
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
