import unittest
from unittest.mock import Mock, patch
from src.api.get_api import GetNoteAPI

class TestGetNoteAPI(unittest.TestCase):
    """
    测试Get笔记API连接模块
    """
    
    @patch('src.api.get_api.requests.post')
    def test_search_notes_success(self, mock_post):
        """
        测试搜索笔记成功的情况
        """
        # 模拟API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'documents': [
                {
                    'id': '1',
                    'title': '测试笔记1',
                    'content': '测试内容1',
                    'score': 0.9
                },
                {
                    'id': '2',
                    'title': '测试笔记2',
                    'content': '测试内容2',
                    'score': 0.8
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # 创建API实例
        api = GetNoteAPI()
        
        # 调用搜索方法
        result = api.search_notes('测试查询')
        
        # 验证结果
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], '测试笔记1')
    
    @patch('src.api.get_api.requests.post')
    def test_search_notes_timeout(self, mock_post):
        """
        测试搜索笔记超时的情况
        """
        # 模拟超时异常
        mock_post.side_effect = Exception('Connection timed out')
        
        # 创建API实例
        api = GetNoteAPI()
        
        # 验证异常
        with self.assertRaises(Exception) as context:
            api.search_notes('测试查询')
        self.assertIn('API请求超时', str(context.exception))
    
    @patch('src.api.get_api.requests.get')
    def test_get_note_detail_success(self, mock_get):
        """
        测试获取笔记详情成功的情况
        """
        # 模拟API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': '1',
            'title': '测试笔记',
            'content': '测试内容',
            'created_at': '2023-01-01T00:00:00Z'
        }
        mock_get.return_value = mock_response
        
        # 创建API实例
        api = GetNoteAPI()
        
        # 调用获取详情方法
        result = api.get_note_detail('1')
        
        # 验证结果
        self.assertEqual(result['id'], '1')
        self.assertEqual(result['title'], '测试笔记')

if __name__ == '__main__':
    unittest.main()
