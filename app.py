from hate_spech.pipeline.train_pipeline import TrainPipeline


if __name__ == "__main__":
    print("Starting pipeline...")
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
    print("Pipeline completed.")
