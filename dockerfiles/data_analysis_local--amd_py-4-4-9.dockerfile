FROM quay.io/jupyter/scipy-notebook:lab-4.4.9
RUN pip install py4j

COPY PyBacmman /home/jovyan/work/PyBacmman
USER root
RUN chown -R jovyan:users /home/jovyan/work
USER jovyan
RUN pip install /home/jovyan/work/PyBacmman

# Override settings: dark theme
RUN mkdir -p /opt/conda/share/jupyter/lab/settings
RUN echo '{"@jupyterlab/apputils-extension:themes": {"theme": "JupyterLab Dark"}}' > /opt/conda/share/jupyter/lab/settings/overrides.json

# create working dir
USER root
RUN mkdir -p /data
RUN chmod 777 /data
RUN chown -R $NB_UID:$NB_GID /data
USER $NB_UID
WORKDIR /data