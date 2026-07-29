import { Component, computed, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

type Availability = 'Available' | 'Focused';
type Filter = 'All' | Availability;

interface TeamMember {
  id: number; name: string; role: string; availability: Availability; tasks: number;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly filters: Filter[] = ['All', 'Available', 'Focused'];
  protected readonly activeFilter = signal<Filter>('All');
  protected readonly members = signal<TeamMember[]>([
    { id: 1, name: 'Maya Chen', role: 'Product Designer', availability: 'Available', tasks: 3 },
    { id: 2, name: 'Noah Williams', role: 'Frontend Engineer', availability: 'Focused', tasks: 5 },
    { id: 3, name: 'Isha Rao', role: 'QA Engineer', availability: 'Available', tasks: 2 },
    { id: 4, name: 'Leo Martin', role: 'Backend Engineer', availability: 'Focused', tasks: 4 }
  ]);
  protected newMemberName = '';
  protected newMemberRole = '';
  private nextId = 5;

  protected readonly availableCount = computed(() => this.members().filter((member) => member.availability === 'Available').length);
  protected readonly totalTasks = computed(() => this.members().reduce((total, member) => total + member.tasks, 0));
  protected readonly capacity = computed(() => Math.round((this.availableCount() / this.members().length) * 100));
  protected readonly visibleMembers = computed(() => {
    const filter = this.activeFilter();
    return filter === 'All' ? this.members() : this.members().filter((member) => member.availability === filter);
  });

  protected setFilter(filter: Filter): void { this.activeFilter.set(filter); }

  protected toggleAvailability(id: number): void {
    this.members.update((members) => members.map((member) =>
      member.id === id
        ? { ...member, availability: member.availability === 'Available' ? 'Focused' : 'Available' }
        : member
    ));
  }

  protected addMember(): void {
    const name = this.newMemberName.trim();
    const role = this.newMemberRole.trim();
    if (!name || !role) return;
    this.members.update((members) => [...members, {
      id: this.nextId++, name, role, availability: 'Available', tasks: 0
    }]);
    this.newMemberName = '';
    this.newMemberRole = '';
    this.activeFilter.set('All');
  }
}
