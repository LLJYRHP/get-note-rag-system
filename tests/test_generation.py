import unittest
from unittest.mock import Mock, patch
from src.generation.generator import AnswerGenerator

class TestAnswerGenerator(unittest.TestCase):
    """
    测试回答生成模块
    """
    
    @patch('src.generation.generator.OpenAI')
    def test_generate_with_notes(self, mock_openai):
        """
        测试有相关笔记时的生成情况
        """
        # 模拟LLM响应
        mock_llm = Mock()
        mock_openai.return_value = mock_llm
        mock_llm.__call__.return_value = "这是一个测试回答 [笔记1]"
        
        # 创建生成器实例
        generator = AnswerGenerator()
        
        # 模拟笔记数据
        test_notes = [
            {
                'id': '1',
                'title': '测试笔记1',
                'content': '测试内容1',
                'relevance_score': 0.9
            }
        ]
        
        # 调用生成方法
        result = generator.generate('测试查询', test_notes)
        
        # 验证结果
        self.assertEqual(result['has_relevant_notes'], True)
        self.assertEqual(len(result['references']), 1)
        self.assertIn('笔记1', result['references'][0]['reference_id'])
    
    def test_generate_no_notes(self):
        """
        测试没有相关笔记时的生成情况
        """
        # 创建生成器实例
        generator = AnswerGenerator()
        
        # 调用生成方法（无笔记）
        result = generator.generate('测试查询', [])
        
        # 验证结果
        self.assertEqual(result['has_relevant_notes'], False)
        self.assertEqual(len(result['references']), 0)
        self.assertIn('未检索到与您的问题相关的笔记内容', result['answer'])
    
    def test_build_context(self):
        """
        测试构建上下文功能
        """
        generator = AnswerGenerator()
        test_notes = [
            {
                'id': '1',
                'title': '测试笔记1',
                'content': '测试内容1'
            }
        ]
        context = generator._build_context(test_notes)
        self.assertIn('【笔记1】', context)
        self.assertIn('测试笔记1', context)
        self.assertIn('测试内容1', context)
    
    def test_extract_references(self):
        """
        测试提取引用信息功能
        """
        generator = AnswerGenerator()
        test_notes = [
            {
                'id': '1',
                'title': '测试笔记1',
                'relevance_score': 0.9
            }
        ]
        references = generator._extract_references(test_notes)
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0]['id'], '1')
        self.assertEqual(references[0]['title'], '测试笔记1')
        self.assertEqual(references[0]['reference_id'], '笔记1')

if __name__ == '__main__':
    unittest.main()
