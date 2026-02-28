import unittest
from unittest.mock import Mock, patch
from src.retrieval.retrieval import NoteRetriever

class TestNoteRetriever(unittest.TestCase):
    """
    测试笔记检索模块
    """
    
    @patch('src.retrieval.retrieval.GetNoteAPI')
    def test_retrieve_success(self, mock_api):
        """
        测试检索成功的情况
        """
        # 模拟API响应
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance
        mock_api_instance.search_notes.return_value = [
            {
                'id': '1',
                'title': '测试笔记1',
                'content': '  测试内容1  ',
                'score': 0.9
            },
            {
                'id': '2',
                'title': '测试笔记2',
                'content': '测试内容2\n测试内容3',
                'score': 0.6
            }
        ]
        
        # 创建检索实例
        retriever = NoteRetriever()
        
        # 调用检索方法
        result = retriever.retrieve('测试查询')
        
        # 验证结果
        self.assertEqual(len(result), 1)  # 第二个笔记分数低于阈值0.7
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], '测试笔记1')
        self.assertEqual(result[0]['content'], '测试内容1')  # 验证内容清洗
        self.assertEqual(result[0]['relevance_score'], 0.9)
    
    @patch('src.retrieval.retrieval.GetNoteAPI')
    def test_retrieve_no_results(self, mock_api):
        """
        测试没有检索结果的情况
        """
        # 模拟API响应
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance
        mock_api_instance.search_notes.return_value = []
        
        # 创建检索实例
        retriever = NoteRetriever()
        
        # 调用检索方法
        result = retriever.retrieve('测试查询')
        
        # 验证结果
        self.assertEqual(len(result), 0)
    
    def test_clean_content(self):
        """
        测试内容清洗功能
        """
        retriever = NoteRetriever()
        test_content = '  测试内容1\n测试内容2  '
        cleaned_content = retriever._clean_content(test_content)
        self.assertEqual(cleaned_content, '测试内容1 测试内容2')
    
    def test_get_context(self):
        """
        测试构建上下文功能
        """
        retriever = NoteRetriever()
        test_notes = [
            {
                'id': '1',
                'title': '测试笔记1',
                'content': '测试内容1',
                'relevance_score': 0.9
            }
        ]
        context = retriever.get_context(test_notes)
        self.assertIn('【笔记1】', context)
        self.assertIn('测试笔记1', context)
        self.assertIn('测试内容1', context)

if __name__ == '__main__':
    unittest.main()
