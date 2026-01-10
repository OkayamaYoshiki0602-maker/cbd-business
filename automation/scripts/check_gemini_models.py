#!/usr/bin/env python3
"""
Gemini APIの利用可能なモデルを確認するスクリプト
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

# .envファイルを読み込む
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

def list_gemini_models():
    """利用可能なGeminiモデルをリストアップ"""
    try:
        import google.generativeai as genai
        
        if not GEMINI_API_KEY:
            print("❌ GEMINI_API_KEYが設定されていません")
            print("   .envファイルにGEMINI_API_KEYを設定してください")
            return
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        print("🔍 Gemini APIの利用可能なモデルを確認中...\n")
        print("=" * 60)
        
        models = genai.list_models()
        
        # generateContentをサポートするモデルをフィルタ
        content_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
        
        print(f"✅ 利用可能なモデル: {len(content_models)}件\n")
        
        for i, model in enumerate(content_models, 1):
            print(f"{i}. モデル名: {model.name}")
            print(f"   表示名: {model.display_name}")
            if hasattr(model, 'description') and model.description:
                print(f"   説明: {model.description}")
            print(f"   サポートメソッド: {', '.join(model.supported_generation_methods)}")
            print()
        
        print("=" * 60)
        print("\n📝 推奨モデル名（コードで使用）:\n")
        
        # よく使われるモデル名の形式を表示
        for model in content_models[:5]:  # 最初の5件を表示
            # モデル名から短縮形を抽出
            model_name = model.name
            if '/' in model_name:
                short_name = model_name.split('/')[-1]
            else:
                short_name = model_name
            
            print(f"  - {short_name}")
            print(f"    (完全名: {model_name})")
        
        # テスト: 実際にモデルを使用してみる
        print("\n🧪 モデルをテスト中...\n")
        
        test_models = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
            'gemini-2.0-flash-exp',
        ]
        
        for model_name in test_models:
            try:
                print(f"テスト: {model_name}...", end=' ')
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello")
                print("✅ 成功")
            except Exception as e:
                error_msg = str(e)
                if '404' in error_msg:
                    print(f"❌ 404 (モデルが見つかりません)")
                elif '403' in error_msg:
                    print(f"⚠️ 403 (権限エラー)")
                else:
                    print(f"❌ エラー: {error_msg[:50]}")
        
        print("\n✅ 確認完了")
        
    except ImportError:
        print("❌ google-generativeaiライブラリがインストールされていません")
        print("   以下のコマンドでインストールしてください:")
        print("   pip install google-generativeai")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    list_gemini_models()
