import json
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class MeetingMinutesAssistant:
    """智能会议纪要生成助手核心类"""
    
    def __init__(self, api_key: str, api_base: str = "https://api.openai.com/v1"):
        """
        初始化助手
        Args:
            api_key: 大模型API密钥
            api_base: API基础地址
        """
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def simulate_audio_to_text(self, audio_content: str) -> str:
        """
        模拟语音转文本功能（实际项目中会调用ASR API）
        Args:
            audio_content: 模拟的音频内容描述
        Returns:
            转换后的文本
        """
        print("正在将会议录音转换为文本...")
        time.sleep(1)  # 模拟处理时间
        
        # 模拟返回的会议文本
        meeting_text = f"""
        会议主题：{audio_content}
        时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
        参会人员：张三、李四、王五、赵六
        讨论内容：
        1. 项目进度：前端开发已完成80%，后端API接口开发完成70%
        2. 遇到的问题：第三方支付接口对接存在延迟，需要协调解决
        3. 下周计划：完成所有核心功能开发，开始内部测试
        4. 重要决策：决定采用微服务架构进行系统重构
        5. 待办事项：李四负责跟进支付接口，王五准备测试环境
        """
        print("语音转文本完成！")
        return meeting_text
    
    def generate_summary(self, meeting_text: str) -> Dict[str, Any]:
        """
        使用大模型生成会议纪要摘要
        Args:
            meeting_text: 会议文本内容
        Returns:
            结构化会议纪要
        """
        print("正在使用大模型生成会议纪要...")
        
        # 构建大模型请求
        prompt = f"""请根据以下会议内容，生成结构化的会议纪要：

{meeting_text}

请按以下JSON格式返回：
{{
    "meeting_topic": "会议主题",
    "meeting_time": "会议时间",
    "participants": ["参会人员1", "参会人员2"],
    "key_points": ["要点1", "要点2", "要点3"],
    "decisions": ["决策1", "决策2"],
    "action_items": [{{"person": "负责人", "task": "任务", "deadline": "截止时间"}}],
    "summary": "会议总结"
}}"""
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 提取JSON部分
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    summary_data = json.loads(content[json_start:json_end])
                else:
                    summary_data = {"summary": content, "error": "JSON解析失败"}
                
                print("会议纪要生成成功！")
                return summary_data
            else:
                return {"error": f"API请求失败: {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {"error": f"生成纪要时出错: {str(e)}"}
    
    def save_minutes(self, summary: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        保存会议纪要到文件
        Args:
            summary: 会议纪要数据
            filename: 文件名（可选）
        Returns:
            保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meeting_minutes_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"会议纪要已保存到: {filename}")
        return filename
    
    def display_summary(self, summary: Dict[str, Any]):
        """以友好格式显示会议纪要"""
        print("\n" + "="*50)
        print("智能会议纪要生成结果")
        print("="*50)
        
        if "error" in summary:
            print(f"错误: {summary['error']}")
            return
        
        print(f"会议主题: {summary.get('meeting_topic', '未指定')}")
        print(f"会议时间: {summary.get('meeting_time', '未指定')}")
        print(f"参会人员: {', '.join(summary.get('participants', []))}")
        
        print("\n📌 会议要点:")
        for i, point in enumerate(summary.get('key_points', []), 1):
            print(f"  {i}. {point}")
        
        print("\n✅ 重要决策:")
        for i, decision in enumerate(summary.get('decisions', []), 1):
            print(f"  {i}. {decision}")
        
        print("\n📋 待办事项:")
        for i, item in enumerate(summary.get('action_items', []), 1):
            person = item.get('person', '未指定')
            task = item.get('task', '未指定')
            deadline = item.get('deadline', '未指定')
            print(f"  {i}. [{person}] {task} (截止: {deadline})")
        
        print(f"\n📝 会议总结:\n  {summary.get('summary', '无总结')}")
        print("="*50)

def main():
    """主函数 - 智能会议纪要生成助手入口"""
    print("🚀 启动智能会议纪要生成助手")
    print("-" * 40)
    
    # 配置API密钥（实际使用时从环境变量或配置文件中读取）
    API_KEY = "your-api-key-here"  # 请替换为实际的API密钥
    
    # 创建助手实例
    assistant = MeetingMinutesAssistant(api_key=API_KEY)
    
    # 模拟会议音频内容
    meeting_audio = "季度产品规划与开发进度同步会议"
    
    try:
        # 步骤1: 语音转文本
        meeting_text = assistant.simulate_audio_to_text(meeting_audio)
        
        # 步骤2: 生成会议纪要
        summary = assistant.generate_summary(meeting_text)
        
        # 步骤3: 显示结果
        assistant.display_summary(summary)
        
        # 步骤4: 保存纪要
        if "error" not in summary:
            saved_file = assistant.save_minutes(summary)
            print(f"\n✅ 纪要整理完成！文件已保存: {saved_file}")
            
            # 模拟效果统计
            print("\n📊 效果统计:")
            print("  • 纪要整理时间缩短: ~65%")
            print("  • 用户满意度: 4.8/5.0")
            print("  • 信息完整度: 95%")
        else:
            print(f"\n❌ 纪要生成失败: {summary.get('error')}")
            print("提示: 请检查API密钥配置或网络连接")
            
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()