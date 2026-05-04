<script lang="ts">
	import { X, Sun, Moon, Globe, GitFork, Coffee } from '@lucide/svelte';
	import type { Theme } from '$lib/player/types';

	type Props = {
		show: boolean;
		theme: Theme;
		onclose: () => void;
		onToggleTheme: () => void;
	};

	let { show, theme, onclose, onToggleTheme }: Props = $props();

	// --- Swipe-to-dismiss ---
	const DISMISS_THRESHOLD_PX = 80;
	const DISMISS_VELOCITY = 0.5;

	let dragY = $state(0);
	let dragging = $state(false);
	let startY = 0;
	let startTime = 0;

	function onDragStart(e: PointerEvent) {
		dragging = true;
		startY = e.clientY;
		startTime = e.timeStamp;
		dragY = 0;
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
	}

	function onDragMove(e: PointerEvent) {
		if (!dragging) return;
		dragY = Math.max(0, e.clientY - startY);
	}

	function onDragEnd(e: PointerEvent) {
		if (!dragging) return;
		dragging = false;
		const velocity = e.timeStamp - startTime > 0 ? dragY / (e.timeStamp - startTime) : 0;
		if (dragY >= DISMISS_THRESHOLD_PX || velocity >= DISMISS_VELOCITY) {
			dragY = window.innerHeight;
			setTimeout(() => { onclose(); dragY = 0; }, 220);
		} else {
			dragY = 0;
		}
	}

	function handleOverlayClick(e: MouseEvent) {
		if (e.target === e.currentTarget) onclose();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') onclose();
	}

	const links = [
		{ label: 'SynapSeq Site', href: 'https://synapseq.org', icon: Globe },
		{ label: 'Repository', href: 'https://github.com/synapseq-foundation/synapseq-hub', icon: GitFork },
		{ label: 'Buy me a Coffee', href: 'https://buymeacoffee.com/ruankleinb', icon: Coffee }
	] as const;
</script>

{#if show}
	<div
		class="fixed inset-0 z-[60] flex items-end justify-center"
		role="dialog"
		aria-modal="true"
		aria-label="Menu"
		tabindex="-1"
		onclick={handleOverlayClick}
		onkeydown={handleKeydown}
	>
		<div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

		<div
			class="relative z-10 w-full overflow-hidden rounded-t-[28px] border border-[var(--line)] bg-[var(--panel-strong)] shadow-[0_-8px_48px_rgba(0,0,0,0.22)]"
			style="transform: translateY({dragY}px); transition: {dragging ? 'none' : 'transform 0.22s cubic-bezier(0.32,0.72,0,1)'};"
		>
			<!-- Drag handle -->
			<div
				class="flex touch-none justify-center pt-3 pb-1"
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
				onclick={onclose}
				aria-label="Close menu"
			>
				<X size={16} />
			</button>

			<div class="px-4 pt-3 pb-[max(1.5rem,env(safe-area-inset-bottom,0px))]">

				<!-- Section: Configuration -->
				<p class="mb-2 px-1 text-[0.68rem] font-[600] uppercase tracking-[0.14em] text-[var(--muted)]">
					Configuration
				</p>

				<button
					class="flex w-full cursor-pointer items-center gap-3 rounded-2xl border border-transparent px-3.5 py-3 text-left transition-all duration-150 hover:border-[var(--line)] hover:bg-[var(--panel-strong)] active:scale-[0.98]"
					onclick={() => { onToggleTheme(); onclose(); }}
				>
					<span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[var(--line)] bg-[var(--bg)] text-[var(--text)]">
						{#if theme === 'dark'}
							<Sun size={16} />
						{:else}
							<Moon size={16} />
						{/if}
					</span>
					<span class="text-[0.92rem] font-[540] text-[var(--text)]">
						{theme === 'dark' ? 'Light Theme' : 'Dark Theme'}
					</span>
				</button>

				<!-- Divider -->
				<div class="my-3 h-px bg-[var(--line)]"></div>

				<!-- Section: Links -->
				<p class="mb-2 px-1 text-[0.68rem] font-[600] uppercase tracking-[0.14em] text-[var(--muted)]">
					Links
				</p>

				{#each links as link (link.href)}
					<a
						href={link.href}
						target="_blank"
						rel="noopener noreferrer"
						class="flex items-center gap-3 rounded-2xl border border-transparent px-3.5 py-3 transition-all duration-150 hover:border-[var(--line)] hover:bg-[var(--panel-strong)] active:scale-[0.98]"
						onclick={onclose}
					>
						<span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[var(--line)] bg-[var(--bg)] text-[var(--muted)]">
							<link.icon size={16} />
						</span>
						<span class="text-[0.92rem] font-[540] text-[var(--text)]">{link.label}</span>
					</a>
				{/each}
			</div>
		</div>
	</div>
{/if}
