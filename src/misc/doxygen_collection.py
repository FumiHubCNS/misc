"""!
@file doxygen_collection.py
@version 1
@author Fumitaka ENDO
@date 2025-06-29T17:08:19+09:00
@brief template text
"""
import tomllib
import pathlib
import shutil
from pathlib import Path

this_file_path = pathlib.Path(__file__).parent

def copy_inputs_to_output(input_list, output_path, flag=False):
	output_path = Path(output_path)
	output_path.mkdir(parents=True, exist_ok=True)

	for input_dir in input_list:
		input_path = Path(input_dir).resolve()

		if not input_path.is_dir():
			print(f"スキップ: {input_path} はディレクトリではありません")
			continue

		# 2階層上のディレクトリ名をコピー先の名前として使う
		try:
			new_dirname = input_path.parents[0].name
		except IndexError:
			print(f"スキップ: {input_path} の2階層上が存在しません")
			continue

		destination = output_path / new_dirname

		if flag:
			if destination.exists():
				print(f"削除して再コピー: {destination}")
				shutil.rmtree(destination)
			shutil.copytree(input_path, destination)
			print(f"コピー完了: {input_path} → {destination}")
		else:
			print(destination)

def read_config(path):
    with open(path, 'rb') as f:
        config = tomllib.load(f)
    return config	

def copy_doxygens():
	input_path = this_file_path / '../../param/doxygen-list.toml'
	config = read_config(input_path)
	input_list = config["doxygen"]["inputs"]
	output_path = config["doxygen"]["output_path"].strip()
	copy_inputs_to_output(input_list, output_path, True)
	
if __name__ == '__main__':
	input_path = this_file_path / '../../param/doxygen-list.toml'
	config = read_config(input_path)
	input_list = config["doxygen"]["inputs"]
	output_path = config["doxygen"]["output_path"].strip()
	copy_inputs_to_output(input_list, output_path, False)
