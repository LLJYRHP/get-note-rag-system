from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from typing import Dict, List, Any
from src.utils.logger import get_logger

# 初始化日志
logger = get_logger(__name__)

class AnswerGenerator:
    """
    增强生成模块
    基于检索到的笔记内容生成准确、有依据的回答
    """
    
    def __init__(self):
        """
        初始化生成模块
        """
        # 这里使用OpenAI作为示例，实际部署时可以替换为其他LLM
        # 注意：需要在环境变量中设置OPENAI_API_KEY
        self.llm = OpenAI(temperature=0.3)
        self.prompt_template = self._create_prompt_template()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def _create_prompt_template(self) -> PromptTemplate:
        """
        创建提示模板
        
        Returns:
            提示模板对象
        """
        template = """
你是一个基于Get笔记内容的问答助手，需要严格基于提供的笔记内容回答用户问题。

请按照以下要求回答：
1. 严格基于提供的笔记内容，不要添加任何笔记中没有的信息
2. 明确标注引用来源，格式为：[笔记X]，其中X是笔记的编号
3. 对引用的内容进行高亮显示
4. 当检索不到相关笔记时，明确提示并建议调整问题

用户问题：{query}

相关笔记：
{context}

请生成回答：
        """
        
        return PromptTemplate(
            input_variables=["query", "context"],
            template=template
        )
    
    def generate(self, query: str, notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成回答
        
        Args:
            query: 用户查询语句
            notes: 检索到的相关笔记
            
        Returns:
            包含回答和引用信息的字典
        """
        logger.info(f"开始生成回答，查询: {query}, 相关笔记数: {len(notes)}")
        try:
            # 检查是否有相关笔记
            if not notes:
                logger.info("未检索到相关笔记")
                return {
                    "answer": "抱歉，未检索到与您的问题相关的笔记内容。请尝试调整问题表述或提供更多关键词。",
                    "references": [],
                    "has_relevant_notes": False
                }
            
            # 构建上下文
            context = self._build_context(notes)
            
            # 生成回答
            result = self.chain.run(query=query, context=context)
            
            # 提取引用信息
            references = self._extract_references(notes)
            
            logger.info("回答生成完成")
            return {
                "answer": result,
                "references": references,
                "has_relevant_notes": True
            }
            
        except Exception as e:
            logger.error(f"生成回答时发生错误: {e}")
            raise Exception(f"生成回答时发生错误: {e}")
    
    def _build_context(self, notes: List[Dict[str, Any]]) -> str:
        """
        构建上下文
        
        Args:
            notes: 检索到的相关笔记
            
        Returns:
            上下文字符串
        """
        context_parts = []
        
        for i, note in enumerate(notes, 1):
            context_part = f"""
【笔记{i}】
标题: {note['title']}
内容: {note['content']}
            """
            context_parts.append(context_part)
        
        return '\n'.join(context_parts)
    
    def _extract_references(self, notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        提取引用信息
        
        Args:
            notes: 检索到的相关笔记
            
        Returns:
            引用信息列表
        """
        references = []
        
        for i, note in enumerate(notes, 1):
            reference = {
                "id": note['id'],
                "title": note['title'],
                "relevance_score": note['relevance_score'],
                "reference_id": f"笔记{i}"
            }
            references.append(reference)
        
        return references
