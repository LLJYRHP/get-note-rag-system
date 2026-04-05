"""
学习功能扩展演示脚本
包含：自动生成测验题、学习进度追踪、智能问题推荐
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import random

class QuizGenerator:
    """测验题生成模块"""
    
    def __init__(self):
        self.question_types = ['multiple_choice', 'true_false', 'fill_in_blank', 'short_answer']
    
    def generate_quiz(self, notes: List[Dict[str, Any]], 
                     question_type: str = 'multiple_choice',
                     difficulty: str = 'medium',
                     num_questions: int = 5) -> Dict[str, Any]:
        if not notes:
            return {'questions': [], 'total_questions': 0}
        
        questions = []
        for i, note in enumerate(notes[:num_questions]):
            q = self._create_question(note, question_type, i)
            if q:
                questions.append(q)
        
        return {
            'questions': questions,
            'total_questions': len(questions),
            'question_type': question_type,
            'difficulty': difficulty
        }
    
    def _create_question(self, note: Dict, q_type: str, index: int) -> Dict:
        if q_type == 'multiple_choice':
            return self._create_multiple_choice(note, index)
        elif q_type == 'true_false':
            return self._create_true_false(note, index)
        elif q_type == 'fill_in_blank':
            return self._create_fill_in_blank(note, index)
        else:
            return self._create_short_answer(note, index)
    
    def _create_multiple_choice(self, note: Dict, index: int) -> Dict:
        content = note['content']
        words = content.split()
        
        if len(words) > 3:
            correct_answer = ' '.join(words[:3])
            return {
                'id': index,
                'question': f"根据笔记'{note['title']}',以下哪项是正确的？",
                'options': [
                    f"A. {correct_answer}",
                    f"B. {' '.join(words[1:4]) if len(words) > 3 else '干扰项 B'}",
                    f"C. {' '.join(words[2:5]) if len(words) > 4 else '干扰项 C'}",
                    f"D. {' '.join(words[3:6]) if len(words) > 5 else '干扰项 D'}"
                ],
                'answer': 'A',
                'explanation': f"答案来自笔记内容",
                'note_title': note['title']
            }
        return {}
    
    def _create_true_false(self, note: Dict, index: int) -> Dict:
        return {
            'id': index,
            'question': f"笔记'{note['title']}'中包含重要知识点。",
            'options': ['A. 正确', 'B. 错误'],
            'answer': 'A',
            'explanation': '所有笔记都包含有价值的信息',
            'note_title': note['title']
        }
    
    def _create_fill_in_blank(self, note: Dict, index: int) -> Dict:
        content = note['content']
        words = content.split()
        
        if words:
            key_word = words[0]
            return {
                'id': index,
                'question': f"填空：{content.replace(key_word, '_____', 1)}",
                'options': [],
                'answer': key_word,
                'explanation': f"答案来自笔记'{note['title']}'",
                'note_title': note['title']
            }
        return {}
    
    def _create_short_answer(self, note: Dict, index: int) -> Dict:
        return {
            'id': index,
            'question': f"请简述'{note['title']}'的主要内容。",
            'options': [],
            'answer': note['content'][:100] + '...',
            'explanation': '这是一个开放性问题的参考答案',
            'note_title': note['title']
        }
    
    def grade_quiz(self, user_answers: List[str], 
                   correct_answers: List[str], 
                   question_type: str = 'multiple_choice') -> Dict[str, Any]:
        total = len(correct_answers)
        correct = sum(1 for u, c in zip(user_answers, correct_answers) 
                     if u.strip().upper() == c.strip().upper())
        score = (correct / total * 100) if total > 0 else 0
        
        return {
            'total_questions': total,
            'correct_count': correct,
            'score': score,
            'level': '优秀' if score >= 90 else '良好' if score >= 70 else '及格' if score >= 60 else '需努力'
        }


class ProgressTracker:
    """学习进度追踪模块"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.progress_file = os.path.join(self.data_dir, 'learning_progress.json')
        self._init_file()
    
    def _init_file(self):
        if not os.path.exists(self.progress_file):
            self._save_data({'users': {}, 'global_stats': {
                'total_sessions': 0, 'total_time': 0}})
    
    def _load_data(self) -> Dict:
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'users': {}, 'global_stats': {}}
    
    def _save_data(self, data: Dict):
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def record_session(self, user_id: str, topic: str, duration: int = 60):
        data = self._load_data()
        
        if user_id not in data['users']:
            data['users'][user_id] = {
                'created_at': datetime.now().isoformat(),
                'sessions': [],
                'topics': {},
                'total_time': 0,
                'quiz_scores': []
            }
        
        user = data['users'][user_id]
        session = {
            'timestamp': datetime.now().isoformat(),
            'topic': topic,
            'duration': duration
        }
        
        user['sessions'].append(session)
        user['total_time'] += duration
        
        if topic not in user['topics']:
            user['topics'][topic] = {'count': 0, 'time': 0}
        user['topics'][topic]['count'] += 1
        user['topics'][topic]['time'] += duration
        
        data['global_stats']['total_sessions'] += 1
        data['global_stats']['total_time'] += duration
        
        self._save_data(data)
        return session
    
    def get_progress(self, user_id: str) -> Dict:
        data = self._load_data()
        return data['users'].get(user_id, {})
    
    def record_quiz_score(self, user_id: str, score: float, topic: str = ''):
        data = self._load_data()
        
        if user_id in data['users']:
            quiz_record = {
                'timestamp': datetime.now().isoformat(),
                'score': score,
                'topic': topic
            }
            data['users'][user_id]['quiz_scores'].append(quiz_record)
            self._save_data(data)
    
    def get_statistics(self, user_id: str) -> Dict:
        user_data = self.get_progress(user_id)
        if not user_data:
            return {}
        
        sessions = user_data.get('sessions', [])
        quiz_scores = user_data.get('quiz_scores', [])
        
        return {
            'total_sessions': len(sessions),
            'total_time_minutes': user_data.get('total_time', 0) / 60,
            'topics_learned': len(user_data.get('topics', {})),
            'average_quiz_score': sum(q['score'] for q in quiz_scores) / len(quiz_scores) if quiz_scores else 0,
            'recent_topics': list(user_data.get('topics', {}).keys())[:5]
        }


class QuestionRecommender:
    """智能问题推荐模块"""
    
    def __init__(self):
        self.template_questions = [
            "关于{topic}的核心概念是什么？",
            "{topic}的实际应用场景有哪些？",
            "如何深入理解{topic}？",
            "{topic}与其他知识点有什么联系？",
            "学习{topic}时常见的误区有哪些？",
            "{topic}的最佳实践是什么？",
            "如何评估对{topic}的掌握程度？",
            "{topic}的高级技巧有哪些？"
        ]
    
    def recommend_questions(self, user_id: str, 
                           tracker: ProgressTracker,
                           limit: int = 5) -> List[str]:
        user_progress = tracker.get_progress(user_id)
        
        if not user_progress:
            return self._get_general_questions()
        
        topics = list(user_progress.get('topics', {}).keys())
        
        if not topics:
            return self._get_general_questions()
        
        recommendations = []
        for topic in topics:
            for template in random.sample(self.template_questions, min(3, len(self.template_questions))):
                recommendations.append(template.format(topic=topic))
        
        return recommendations[:limit]
    
    def _get_general_questions(self) -> List[str]:
        return [
            "我想学习新知识点，有什么推荐？",
            "如何制定有效的学习计划？",
            "有哪些高效的学习方法？",
            "如何巩固已学知识？",
            "如何将理论知识应用到实践中？"
        ]
    
    def recommend_based_on_quiz(self, quiz_result: Dict, 
                                topic: str) -> List[str]:
        score = quiz_result.get('score', 0)
        recommendations = []
        
        if score < 60:
            recommendations.extend([
                f"关于{topic}的基础知识有哪些？",
                f"如何系统学习{topic}？",
                f"{topic}的入门教程推荐"
            ])
        elif score < 80:
            recommendations.extend([
                f"{topic}的进阶知识点有哪些？",
                f"如何提升对{topic}的理解？",
                f"{topic}的实战练习推荐"
            ])
        else:
            recommendations.extend([
                f"{topic}的高级应用有哪些？",
                f"{topic}的前沿发展是什么？",
                f"如何精通{topic}？"
            ])
        
        return recommendations


def demo_quiz_generator():
    print("\n" + "="*60)
    print("📝 功能演示一：自动生成测验题")
    print("="*60)
    
    sample_notes = [
        {
            'title': 'Python 基础语法',
            'content': 'Python 是一种高级编程语言，具有简洁清晰的语法特点。它支持多种编程范式，包括面向对象和函数式编程。'
        },
        {
            'title': '变量与数据类型',
            'content': 'Python 中的变量不需要显式声明类型。常见数据类型包括整数、浮点数、字符串、列表和字典。'
        },
        {
            'title': '控制流程',
            'content': 'Python 使用 if-elif-else 语句进行条件判断。for 循环和 while 循环用于迭代和重复执行代码块。'
        }
    ]
    
    generator = QuizGenerator()
    
    print("\n1️⃣ 生成选择题:")
    quiz = generator.generate_quiz(sample_notes, 'multiple_choice', 'medium', 3)
    for i, q in enumerate(quiz['questions'], 1):
        print(f"\n  题目{i}: {q['question']}")
        for opt in q['options']:
            print(f"    {opt}")
        print(f"    ✓ 答案：{q['answer']}")
    
    print("\n2️⃣ 生成判断题:")
    quiz = generator.generate_quiz(sample_notes, 'true_false', 'easy', 2)
    for i, q in enumerate(quiz['questions'], 1):
        print(f"\n  题目{i}: {q['question']}")
        print(f"    选项：{', '.join(q['options'])}")
        print(f"    ✓ 答案：{q['answer']}")
    
    print("\n3️⃣ 生成填空题:")
    quiz = generator.generate_quiz(sample_notes, 'fill_in_blank', 'medium', 2)
    for i, q in enumerate(quiz['questions'], 1):
        print(f"\n  题目{i}: {q['question']}")
        print(f"    ✓ 答案：{q['answer']}")
    
    print("\n4️⃣ 生成简答题:")
    quiz = generator.generate_quiz(sample_notes, 'short_answer', 'hard', 2)
    for i, q in enumerate(quiz['questions'], 1):
        print(f"\n  题目{i}: {q['question']}")
        print(f"    ✓ 参考答案：{q['answer']}")
    
    print("\n5️⃣ 测验评分演示:")
    user_answers = ['A', 'A', 'A']
    correct_answers = ['A', 'A', 'B']
    result = generator.grade_quiz(user_answers, correct_answers)
    print(f"    总题数：{result['total_questions']}")
    print(f"    正确数：{result['correct_count']}")
    print(f"    得分：{result['score']:.1f}%")
    print(f"    等级：{result['level']}")


def demo_progress_tracker():
    print("\n" + "="*60)
    print("📊 功能演示二：学习进度追踪")
    print("="*60)
    
    tracker = ProgressTracker()
    user_id = "demo_user"
    
    print("\n1️⃣ 记录学习会话:")
    sessions = [
        ("Python 基础", 1800),
        ("变量与数据类型", 1200),
        ("控制流程", 1500),
        ("函数定义", 2000),
    ]
    
    for topic, duration in sessions:
        session = tracker.record_session(user_id, topic, duration)
        print(f"  ✓ 已记录：{topic} - {duration/60:.0f}分钟")
    
    print("\n2️⃣ 记录测验成绩:")
    scores = [85, 90, 78, 92]
    topics = ["Python 基础", "变量与数据类型", "控制流程", "函数定义"]
    
    for score, topic in zip(scores, topics):
        tracker.record_quiz_score(user_id, score, topic)
        print(f"  ✓ {topic}: {score}分")
    
    print("\n3️⃣ 获取学习统计:")
    stats = tracker.get_statistics(user_id)
    print(f"  📚 学习会话数：{stats['total_sessions']}")
    print(f"  ⏱️  总学习时间：{stats['total_time_minutes']:.1f}分钟")
    print(f"  📖 学习主题数：{stats['topics_learned']}")
    print(f"  📊 平均测验分：{stats['average_quiz_score']:.1f}分")
    print(f"  🏷️  最近主题：{', '.join(stats['recent_topics'])}")


def demo_question_recommender():
    print("\n" + "="*60)
    print("💡 功能演示三：智能问题推荐")
    print("="*60)
    
    tracker = ProgressTracker()
    user_id = "demo_user"
    recommender = QuestionRecommender()
    
    tracker.record_session(user_id, "Python 编程", 1800)
    tracker.record_session(user_id, "数据分析", 2400)
    tracker.record_quiz_score(user_id, 75, "Python 编程")
    
    print("\n1️⃣ 基于学习历史推荐:")
    recommendations = recommender.recommend_questions(user_id, tracker, 5)
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("\n2️⃣ 基于测验成绩推荐 (75 分):")
    quiz_result = {'score': 75}
    recommendations = recommender.recommend_based_on_quiz(quiz_result, "Python 编程")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("\n3️⃣ 基于优秀成绩推荐 (95 分):")
    quiz_result = {'score': 95}
    recommendations = recommender.recommend_based_on_quiz(quiz_result, "数据分析")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")


def main():
    print("\n" + "🎓"*30)
    print("   Get 笔记 RAG 问答系统 - 学习功能扩展演示")
    print("🎓"*30)
    
    print("\n本演示展示三个核心学习功能:")
    print("  1. 📝 自动生成测验题 (选择题/判断题/填空题/简答题)")
    print("  2. 📊 学习进度追踪 (会话记录/成绩统计)")
    print("  3. 💡 智能问题推荐 (基于历史/基于成绩)")
    
    try:
        demo_quiz_generator()
        demo_progress_tracker()
        demo_question_recommender()
        
        print("\n" + "="*60)
        print("✅ 所有功能演示完成!")
        print("="*60)
        print("\n💡 提示:")
        print("  - 测验数据已保存到 data/learning_progress.json")
        print("  - 可以将这些功能集成到主应用 app.py 中")
        print("  - 查看代码了解如何调用这些功能")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()