<script lang="ts">
	import { defaultArtwork } from '$lib/player/constants';
</script>

<div class="fixed inset-0 z-[60] flex items-center justify-center bg-[var(--bg)] backdrop-blur-md">
	<div class="flex flex-col items-center gap-6">
		<!-- Logo with pulse glow -->
		<div class="relative">
			<div class="absolute inset-0 animate-ping rounded-2xl bg-[var(--accent-soft)] opacity-60" style="animation-duration: 2s;"></div>
			<div class="absolute inset-[-6px] rounded-[22px] bg-[var(--accent-soft)] blur-[14px]"></div>
			<img
				src={defaultArtwork}
				alt="SynapSeq"
				class="relative h-[72px] w-[72px] rounded-2xl border border-[var(--line-strong)] object-cover shadow-lg"
			/>
		</div>

		<!-- Waveform bars -->
		<div class="flex items-end gap-[5px]" aria-hidden="true">
			{#each [0, 1, 2, 3, 4] as i}
				<div
					class="w-[4px] rounded-full bg-[var(--accent)]"
					style="
						height: {[18, 28, 22, 32, 16][i]}px;
						animation: wave 1.1s ease-in-out infinite;
						animation-delay: {i * 0.13}s;
						opacity: 0.85;
					"
				></div>
			{/each}
		</div>

		<!-- Label -->
		<p class="text-[0.8rem] font-[500] uppercase tracking-[0.14em] text-[var(--muted)]">
			Loading catalog…
		</p>
	</div>
</div>

<style>
	@keyframes wave {
		0%, 100% { transform: scaleY(0.4); }
		50%       { transform: scaleY(1); }
	}
</style>
