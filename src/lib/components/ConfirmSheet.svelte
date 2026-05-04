<script lang="ts">
	import { X } from '@lucide/svelte';

	type Props = {
		show: boolean;
		title: string;
		description: string;
		confirmLabel?: string;
		cancelLabel?: string;
		onconfirm: () => void;
		oncancel: () => void;
	};

	let {
		show,
		title,
		description,
		confirmLabel = 'Confirm',
		cancelLabel = 'Cancel',
		onconfirm,
		oncancel
	}: Props = $props();

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
			setTimeout(() => { oncancel(); dragY = 0; }, 220);
		} else {
			dragY = 0;
		}
	}

	function handleOverlayClick(e: MouseEvent) {
		if (e.target === e.currentTarget) oncancel();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') oncancel();
	}
</script>

{#if show}
	<div
		class="fixed inset-0 z-[60] flex items-end justify-center sm:items-center"
		role="dialog"
		aria-modal="true"
		aria-label={title}
		tabindex="-1"
		onclick={handleOverlayClick}
		onkeydown={handleKeydown}
	>
		<div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

		<div
			class="relative z-10 w-full overflow-hidden rounded-t-[28px] border border-[var(--line)] bg-[var(--panel-strong)] shadow-[0_-8px_48px_rgba(0,0,0,0.22)] sm:mx-4 sm:max-w-sm sm:rounded-[28px] sm:shadow-[var(--shadow)]"
			style="transform: translateY({dragY}px); transition: {dragging ? 'none' : 'transform 0.22s cubic-bezier(0.32,0.72,0,1)'};"
		>
			<!-- Drag handle -->
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
				onclick={oncancel}
				aria-label="Cancel"
			>
				<X size={16} />
			</button>

			<div class="px-5 pt-4 pb-8 sm:px-6 sm:pt-5 sm:pb-8">
				<h2 class="m-0 mb-2 text-[1.05rem] font-[740] tracking-[-0.03em] text-[var(--text)]">
					{title}
				</h2>
				<p class="m-0 mb-6 text-[0.88rem] leading-relaxed text-[var(--muted)]">
					{description}
				</p>

				<div class="flex gap-3">
					<button
						class="flex-1 cursor-pointer rounded-2xl border border-[var(--line)] bg-transparent py-3 text-[0.9rem] font-[600] text-[var(--muted)] transition-all duration-150 hover:border-[var(--line-strong)] hover:text-[var(--text)] active:scale-[0.98]"
						onclick={oncancel}
					>
						{cancelLabel}
					</button>
					<button
						class="flex-1 cursor-pointer rounded-2xl border border-transparent bg-[var(--accent)] py-3 text-[0.9rem] font-[660] text-[#fffaf1] shadow-[0_2px_12px_rgba(177,77,42,0.35)] transition-all duration-150 hover:-translate-y-px hover:bg-[var(--accent-strong)] active:scale-[0.98]"
						onclick={onconfirm}
					>
						{confirmLabel}
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
