import os
import markdown2  # Markdown 변환 라이브러리
from weasyprint import HTML  # HTML을 PDF로 변환
import logging
from PyPDF2 import PdfMerger
from PIL import Image

# 출력 디렉토리 설정
OUTPUT_DIR = "results/final_reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_report(state):
    """
    보고서를 생성하는 함수. state 객체를 기반으로 Markdown 및 PDF 보고서를 생성합니다.

    Args:
        state (dict): Supervisor에서 전달받은 상태 객체

    Returns:
        dict: 업데이트된 state 객체
    """
    try:
        # 서론 생성
        intro_text = generate_intro(state)

        # Markdown 형식으로 보고서 내용 생성
        markdown_text = f"""
##배터리 시장 트랜드 분석 보고서

### 1. 서론
{intro_text}

### 2. 기업 분석 결과
{format_section(state.get('company_data', '결과 없음'))}

### 3. 시장 분석 결과
{format_section(state.get('market_data', '결과 없음'))}

### 4. 주가 예측 결과
{format_section(state.get('stock_data', '결과 없음'))}

### 5. 주가 예측 그래프
{format_visualization(state.get('visualization_data', '결과 없음'))}
        """

        # Markdown을 HTML로 변환
        html_content = markdown_to_html(markdown_text)

        # HTML 파일 저장 (디버깅용)
        output_html_path = os.path.join(OUTPUT_DIR, "Battery_Industry_Report.html")
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info(f"HTML 보고서가 저장되었습니다: {output_html_path}")

        # PDF 저장
        output_pdf_path = os.path.join(OUTPUT_DIR, "Battery_Industry_Report.pdf")
        save_html_to_pdf(html_content, output_pdf_path)
        logging.info(f"PDF 보고서가 저장되었습니다: {output_pdf_path}")

        # 결과를 state에 저장
        state["report"] = {
            "file_path": output_pdf_path,
            "summary": markdown_text
        }
    except Exception as e:
        logging.error(f"레포트 생성 중 오류가 발생했습니다: {str(e)}")
        state["report"] = {"error": str(e)}

    return state

def generate_intro(state):
    """
    보고서 서론을 생성하는 함수.

    Args:
        state (dict): Supervisor에서 전달받은 상태 객체

    Returns:
        str: 서론 텍스트
    """
    # 기업 이름 추출
    company_names = list(state.get('company_data', {}).keys())
    if not company_names:
        company_names = ["Samsung SDI", "LG에너지솔루션", "동원시스템즈"]

    # 시장 키워드 추출
    market_keyword = state.get('market_data', {}).get('keyword', '배터리 산업')

    # 서론 텍스트 생성
    intro_text = (
        f"{market_keyword}은 전기차와 에너지 저장 시스템(ESS) 시장의 성장과 함께 급격히 발전하고 있습니다. "
        f"본 보고서는 {', '.join(company_names)}를 중심으로 기업 분석, 시장 분석, 주가 예측, 그리고 시각화 결과를 종합하여 "
        f"{market_keyword}의 현재와 미래를 조망합니다. 이를 통해 각 기업의 경쟁력과 기술적 강점을 파악하고, 시장에서의 입지를 평가할 수 있습니다."
    )

    return intro_text

def format_section(data):
    """
    데이터를 사람이 읽기 쉬운 Markdown 형식으로 변환합니다.
    """
    if isinstance(data, dict):
        return "\n".join([f"- **{key}**: {value}" for key, value in data.items()])
    elif isinstance(data, list):
        return "\n".join([f"- {item}" for item in data])
    else:
        return str(data)

def format_visualization(data):
    """
    시각화 데이터를 사람이 읽기 쉬운 Markdown 형식으로 변환합니다.
    """
    if isinstance(data, dict):
        visualization_lines = []
        for key, value in data.items():
            # 이미지 경로를 절대 경로로 변환
            image_path = os.path.abspath(value.get("image_path", "이미지 경로 없음"))
            visualization_lines.append(f"- **{key}**: ![이미지]({image_path})")
        return "\n".join(visualization_lines)
    else:
        return "시각화 데이터 없음"

def markdown_to_html(markdown_text):
    """
    Markdown 텍스트를 HTML로 변환하는 함수.
    """
    html_body = markdown2.markdown(markdown_text)
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>배터리 시장 트렌드 분석 보고서</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                text-align: justify; /* 문단 양쪽 정렬 */
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            h1 {{
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 10px;
            }}
            h2 {{
                text-align: center; /* 제목 가운데 정렬 */
            }}
            ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 5px;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    return html_template


def save_html_to_pdf(html_content, output_pdf_path, visualization_images=None):
    """
    HTML 콘텐츠를 PDF로 저장하고, 그래프 이미지를 PDF의 마지막에 추가하는 함수.

    Args:
        html_content (str): HTML 콘텐츠.
        output_pdf_path (str): 최종 PDF 파일 경로.
        visualization_images (list): 추가할 그래프 이미지 경로 리스트.
    """
    # 1. HTML을 PDF로 변환
    temp_pdf_path = output_pdf_path.replace(".pdf", "_temp.pdf")
    HTML(string=html_content).write_pdf(temp_pdf_path)

    # 2. 그래프 이미지를 PDF로 변환
    image_pdfs = []
    if visualization_images:
        for image_path in visualization_images:
            try:
                # 이미지 파일을 PDF로 변환
                image = Image.open(image_path)
                image_pdf_path = image_path.replace(".png", ".pdf").replace(".jpg", ".pdf")
                image.convert("RGB").save(image_pdf_path)
                image_pdfs.append(image_pdf_path)
            except Exception as e:
                logging.error(f"이미지 변환 중 오류 발생: {image_path}, {str(e)}")

    # 3. PDF 병합
    merger = PdfMerger()
    merger.append(temp_pdf_path)  # HTML로 생성된 PDF 추가
    for image_pdf in image_pdfs:
        merger.append(image_pdf)  # 이미지 PDF 추가
    merger.write(output_pdf_path)
    merger.close()

    # 4. 임시 파일 삭제
    os.remove(temp_pdf_path)
    for image_pdf in image_pdfs:
        os.remove(image_pdf)