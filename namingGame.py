import random
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, id, memory_size=10):
        self.id = id
        self.memory = []
        self.memory_size = memory_size
        self.neighbors = []

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def add_word(self, word):
        if len(self.memory) < self.memory_size:
            if word not in self.memory:
                self.memory.append(word)
        else:
            # Nếu bộ nhớ đầy, xóa từ cũ nhất
            if word not in self.memory:
                self.memory.pop(0)
                self.memory.append(word)

    def get_random_word(self):
        return random.choice(self.memory) if self.memory else None

    def reinforce_word(self, word):
        if word in self.memory:
            self.memory.remove(word)
            self.memory.append(word)  # Đưa từ lên đầu bộ nhớ

class NamingGame:
    def __init__(self, num_agents=6):
        self.agents = [Agent(i) for i in range(num_agents)]
        self.word_counter = 0
        self.history = []
        
        # Tạo mạng lattice với kết nối chu kỳ
        for i in range(num_agents):
            # Kết nối với láng giềng trái
            self.agents[i].add_neighbor(self.agents[(i-1) % num_agents])
            # Kết nối với láng giềng phải
            self.agents[i].add_neighbor(self.agents[(i+1) % num_agents])

    def create_new_word(self):
        self.word_counter += 1
        return f"T{self.word_counter}"

    def step(self):
        # Chọn speaker ngẫu nhiên
        speaker = random.choice(self.agents)
        # Chọn hearer từ láng giềng
        hearer = random.choice(speaker.neighbors)
        
        # Nếu speaker không có từ nào trong bộ nhớ
        if not speaker.memory:
            new_word = self.create_new_word()
            speaker.add_word(new_word)
            hearer.add_word(new_word)
        else:
            # Speaker chọn từ ngẫu nhiên từ bộ nhớ
            chosen_word = speaker.get_random_word()
            
            # Nếu hearer cũng biết từ này
            if chosen_word in hearer.memory:
                speaker.reinforce_word(chosen_word)
                hearer.reinforce_word(chosen_word)
            else:
                # Hearer học từ mới
                hearer.add_word(chosen_word)

        # Lưu trạng thái hiện tại
        self.record_state()

    def get_most_common_word(self):
        # Tìm từ phổ biến nhất trong toàn mạng
        all_words = []
        for agent in self.agents:
            all_words.extend(agent.memory)
        if not all_words:
            return None
        return max(set(all_words), key=all_words.count)

    def count_agents_with_word(self, word):
        # Đếm số agent có từ được chọn
        return sum(1 for agent in self.agents if word in agent.memory)

    def record_state(self):
        most_common = self.get_most_common_word()
        if most_common:
            count = self.count_agents_with_word(most_common)
            self.history.append(count)

    def simulate(self, steps):
        for _ in range(steps):
            self.step()

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(self.history)), self.history, '-o')
        plt.title('Quá trình hội tụ trong Naming Game')
        plt.xlabel('Số bước')
        plt.ylabel('Số agent sử dụng từ phổ biến nhất')
        plt.grid(True)
        plt.show()

    def print_state(self):
        print("\nTrạng thái hiện tại của mạng:")
        for agent in self.agents:
            print(f"Agent {agent.id}: {agent.memory}")

# Chạy mô phỏng
game = NamingGame(6)
print("Trạng thái ban đầu:")
game.print_state()

# Mô phỏng 10 bước đầu tiên
for i in range(10):
    print(f"\nBước {i+1}:")
    game.step()
    game.print_state()

# Tiếp tục mô phỏng thêm và vẽ đồ thị
game.simulate(20)
game.plot_results()