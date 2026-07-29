<script lang="ts">
	type Category = 'Deep work' | 'Meeting' | 'Learning';
	type Filter = 'All' | 'Open' | 'Done';

	type Task = {
		id: number;
		title: string;
		category: Category;
		minutes: number;
		done: boolean;
	};

	let tasks = $state<Task[]>([
		{ id: 1, title: 'Plan the product sprint', category: 'Deep work', minutes: 60, done: true },
		{ id: 2, title: 'Review dashboard prototype', category: 'Meeting', minutes: 30, done: false },
		{ id: 3, title: 'Practice Svelte runes', category: 'Learning', minutes: 45, done: false },
		{ id: 4, title: 'Prepare release notes', category: 'Deep work', minutes: 40, done: false }
	]);
	let activeFilter = $state<Filter>('All');
	let newTitle = $state('');
	let newCategory = $state<Category>('Deep work');
	let newMinutes = $state(30);
	let nextId = 5;

	const filters: Filter[] = ['All', 'Open', 'Done'];
	const completedCount = $derived(tasks.filter((task) => task.done).length);
	const focusMinutes = $derived(tasks.reduce((total, task) => total + task.minutes, 0));
	const progress = $derived(tasks.length ? Math.round((completedCount / tasks.length) * 100) : 0);
	const visibleTasks = $derived(
		tasks.filter((task) => {
			if (activeFilter === 'Open') return !task.done;
			if (activeFilter === 'Done') return task.done;
			return true;
		})
	);

	function addTask() {
		const title = newTitle.trim();
		if (!title) return;
		tasks.push({ id: nextId++, title, category: newCategory, minutes: newMinutes, done: false });
		newTitle = '';
		newMinutes = 30;
		activeFilter = 'All';
	}
</script>

<svelte:head>
	<title>Focus Flow Planner</title>
	<meta name="description" content="An interactive Svelte focus planning dashboard" />
</svelte:head>

<main class="shell">
	<header class="hero">
		<div>
			<p class="eyebrow">SvelteJS stimulated task</p>
			<h1>Focus <em>Flow</em> Planner</h1>
			<p class="intro">Turn your priorities into a calm, achievable day.</p>
		</div>
		<div class="date-card">
			<span>Today</span><strong
				>{new Intl.DateTimeFormat('en', { weekday: 'long' }).format(new Date())}</strong
			>
		</div>
	</header>

	<section class="summary" aria-label="Daily summary">
		<article><span>Tasks planned</span><strong>{tasks.length}</strong></article>
		<article><span>Completed</span><strong>{completedCount}</strong></article>
		<article><span>Focus time</span><strong>{focusMinutes}<small> min</small></strong></article>
		<article class="progress-card">
			<div><span>Daily progress</span><strong>{progress}%</strong></div>
			<div class="progress"><i style:width={progress + '%'}></i></div>
		</article>
	</section>

	<section class="workspace">
		<aside class="composer">
			<p class="section-label">New priority</p>
			<h2>Build your flow</h2>
			<p>Add one clear task and give it a realistic time box.</p>
			<form
				onsubmit={(event) => {
					event.preventDefault();
					addTask();
				}}
			>
				<label
					>Task<input
						bind:value={newTitle}
						placeholder="What needs your attention?"
						required
					/></label
				>
				<div class="form-row">
					<label
						>Type<select bind:value={newCategory}
							><option>Deep work</option><option>Meeting</option><option>Learning</option></select
						></label
					>
					<label
						>Minutes<input
							type="number"
							bind:value={newMinutes}
							min="5"
							max="240"
							step="5"
						/></label
					>
				</div>
				<button type="submit">Add to my day <span>→</span></button>
			</form>
		</aside>

		<section class="task-panel">
			<div class="panel-head">
				<div>
					<p class="section-label">Your schedule</p>
					<h2>Today's priorities</h2>
				</div>
				<div class="filters">
					{#each filters as filter (filter)}
						<button class:active={activeFilter === filter} onclick={() => (activeFilter = filter)}
							>{filter}</button
						>
					{/each}
				</div>
			</div>

			<div class="task-list">
				{#each visibleTasks as task (task.id)}
					<article class:done={task.done}>
						<button
							class="check"
							aria-label="Toggle {task.title}"
							onclick={() => (task.done = !task.done)}>{task.done ? '✓' : ''}</button
						>
						<div class="task-copy">
							<h3>{task.title}</h3>
							<span
								class:meeting={task.category === 'Meeting'}
								class:learning={task.category === 'Learning'}>{task.category}</span
							>
						</div>
						<time>{task.minutes} min</time>
					</article>
				{:else}
					<p class="empty">No tasks match this filter.</p>
				{/each}
			</div>
		</section>
	</section>
</main>

<style>
	:global(*) {
		box-sizing: border-box;
	}
	:global(body) {
		margin: 0;
		min-width: 320px;
		min-height: 100vh;
		color: #17201c;
		background: #f1f0e9;
		font-family: Inter, ui-sans-serif, system-ui, sans-serif;
	}
	:global(button),
	:global(input),
	:global(select) {
		font: inherit;
	}
	.shell {
		width: min(1160px, calc(100% - 32px));
		margin: auto;
		padding: 54px 0;
	}
	.hero {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 24px;
		margin-bottom: 32px;
	}
	.eyebrow,
	.section-label {
		margin: 0 0 9px;
		color: #dc5b31;
		font-size: 0.72rem;
		font-weight: 850;
		letter-spacing: 0.16em;
		text-transform: uppercase;
	}
	h1 {
		margin: 0;
		max-width: 720px;
		font-family: Georgia, serif;
		font-size: clamp(3rem, 8vw, 6.4rem);
		font-weight: 500;
		line-height: 0.82;
		letter-spacing: -0.065em;
	}
	h1 em {
		color: #dc5b31;
		font-weight: inherit;
	}
	.intro {
		margin: 22px 0 0;
		color: #69706c;
		font-size: 1.08rem;
	}
	.date-card {
		min-width: 155px;
		padding: 17px 20px;
		border: 1px solid #dcdcd3;
		border-radius: 16px;
		background: #faf9f5;
	}
	.date-card span {
		display: block;
		color: #7c817e;
		font-size: 0.76rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
	}
	.date-card strong {
		display: block;
		margin-top: 5px;
	}
	.summary {
		display: grid;
		grid-template-columns: repeat(3, 1fr) 1.7fr;
		gap: 12px;
		margin-bottom: 18px;
	}
	.summary article,
	.workspace > * {
		border: 1px solid #dedfd7;
		border-radius: 20px;
		background: rgba(255, 255, 252, 0.86);
		box-shadow: 0 18px 50px rgba(40, 50, 44, 0.05);
	}
	.summary article {
		padding: 20px;
	}
	.summary span {
		color: #747b77;
		font-size: 0.82rem;
	}
	.summary strong {
		display: block;
		margin-top: 6px;
		font-size: 1.8rem;
		letter-spacing: -0.04em;
	}
	.summary small {
		font-size: 0.8rem;
		font-weight: 650;
		letter-spacing: 0;
	}
	.progress-card > div:first-child {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.progress-card strong {
		margin: 0;
		font-size: 1.1rem;
	}
	.progress {
		height: 7px;
		margin-top: 14px;
		overflow: hidden;
		border-radius: 99px;
		background: #e7e7df;
	}
	.progress i {
		display: block;
		height: 100%;
		border-radius: inherit;
		background: #dc5b31;
		transition: width 0.3s ease;
	}
	.workspace {
		display: grid;
		grid-template-columns: minmax(270px, 0.72fr) 1.6fr;
		gap: 18px;
	}
	.composer,
	.task-panel {
		padding: 26px;
	}
	h2 {
		margin: 0;
		font-family: Georgia, serif;
		font-size: 1.65rem;
		font-weight: 500;
	}
	.composer > p:not(.section-label) {
		color: #747b77;
		font-size: 0.9rem;
		line-height: 1.6;
	}
	form {
		display: grid;
		gap: 15px;
		margin-top: 25px;
	}
	label {
		display: grid;
		gap: 7px;
		color: #59605c;
		font-size: 0.78rem;
		font-weight: 750;
	}
	input,
	select {
		width: 100%;
		padding: 12px;
		border: 1px solid #d7d9d1;
		border-radius: 10px;
		color: #17201c;
		background: #fff;
		outline: none;
	}
	input:focus,
	select:focus {
		border-color: #dc5b31;
		box-shadow: 0 0 0 3px rgba(220, 91, 49, 0.12);
	}
	.form-row {
		display: grid;
		grid-template-columns: 1.3fr 0.7fr;
		gap: 10px;
	}
	form button {
		display: flex;
		justify-content: space-between;
		padding: 13px 16px;
		border: 0;
		border-radius: 11px;
		color: white;
		background: #1b2922;
		font-weight: 750;
		cursor: pointer;
	}
	.panel-head {
		display: flex;
		align-items: end;
		justify-content: space-between;
		gap: 16px;
		margin-bottom: 23px;
	}
	.filters {
		display: flex;
		gap: 4px;
		padding: 4px;
		border-radius: 10px;
		background: #efefe9;
	}
	.filters button {
		padding: 7px 12px;
		border: 0;
		border-radius: 8px;
		color: #737a76;
		background: transparent;
		cursor: pointer;
		font-size: 0.8rem;
		font-weight: 750;
	}
	.filters button.active {
		color: #17201c;
		background: white;
		box-shadow: 0 2px 8px rgba(40, 50, 44, 0.1);
	}
	.task-list {
		display: grid;
		gap: 9px;
	}
	.task-list article {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 13px;
		padding: 15px;
		border: 1px solid #e4e5de;
		border-radius: 13px;
		background: #fcfcf9;
		transition: opacity 0.2s;
	}
	.task-list article.done {
		opacity: 0.55;
	}
	.task-list article.done h3 {
		text-decoration: line-through;
	}
	.check {
		display: grid;
		place-items: center;
		width: 29px;
		height: 29px;
		border: 1px solid #cfd2ca;
		border-radius: 9px;
		color: white;
		background: white;
		cursor: pointer;
	}
	.done .check {
		border-color: #dc5b31;
		background: #dc5b31;
	}
	.task-copy h3 {
		margin: 0 0 6px;
		font-size: 0.94rem;
	}
	.task-copy span {
		display: inline-block;
		padding: 3px 7px;
		border-radius: 99px;
		color: #367156;
		background: #e0f0e7;
		font-size: 0.67rem;
		font-weight: 750;
	}
	.task-copy span.meeting {
		color: #825020;
		background: #f8ead8;
	}
	.task-copy span.learning {
		color: #4d568b;
		background: #e5e7f6;
	}
	time {
		color: #777e79;
		font-size: 0.78rem;
	}
	.empty {
		padding: 30px;
		color: #777e79;
		text-align: center;
	}
	@media (max-width: 850px) {
		.summary {
			grid-template-columns: repeat(2, 1fr);
		}
		.workspace {
			grid-template-columns: 1fr;
		}
	}
	@media (max-width: 560px) {
		.shell {
			padding: 34px 0;
		}
		.hero,
		.panel-head {
			align-items: stretch;
			flex-direction: column;
		}
		.date-card {
			align-self: flex-start;
		}
		.summary {
			grid-template-columns: 1fr 1fr;
		}
		.summary article,
		.composer,
		.task-panel {
			padding: 17px;
		}
		.filters {
			overflow-x: auto;
		}
	}
</style>
