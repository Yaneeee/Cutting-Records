import streamlit as st
import cv2
import numpy as np

def main():
    st.title("二维码扫描器")

    # 上传图片方式
    uploaded_file = st.file_uploader("上传包含二维码的图片", type=["jpg", "png", "jpeg"])

    # 或使用摄像头（需要Streamlit 1.28+）
    picture = st.camera_input("或用摄像头拍摄二维码")

    # 选择输入源
    img_file = uploaded_file or picture

    if img_file is not None:
        # 将上传的文件转换为OpenCV格式
        file_bytes = np.frombuffer(img_file.getvalue(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # 初始化QRCode检测器
        qr_detector = cv2.QRCodeDetector()
        
        # 检测并解码二维码
        data, bbox, _ = qr_detector.detectAndDecode(img)
        
        if bbox is not None:
            # 绘制检测框
            if len(data) > 0:
                # 将BGR转换为RGB以便在Streamlit中正确显示
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # 绘制边界框
                bbox = bbox[0].astype(int)
                for i in range(len(bbox)):
                    pt1 = tuple(bbox[i])
                    pt2 = tuple(bbox[(i+1) % len(bbox)])
                    cv2.line(img, pt1, pt2, (255, 0, 0), thickness=3)
                
                st.image(img, caption="扫描结果", use_column_width=True)
                st.success(f"解码内容: {data}")
            else:
                st.warning("检测到二维码但无法解码")
        else:
            st.error("未检测到二维码")

if __name__ == "__main__":
    main()