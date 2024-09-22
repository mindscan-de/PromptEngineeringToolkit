pushd
cd %~dp0

SET PYTHONPATH=%~dp0/src/;%PYTHONPATH

cd %~dp0/src/de/mindscan/ai/petk/main

streamlit run ai_petk_app.py --server.port 8585
 
popd