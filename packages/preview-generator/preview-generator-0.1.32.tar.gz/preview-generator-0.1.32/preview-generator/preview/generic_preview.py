import os
from io import BytesIO

import logging
import typing
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

from preview_generator import file_converter

from preview_generator.factory import PreviewBuilderFactory


class PreviewBuilderInterface(object):
    pass


class PreviewBuilderMeta(type):
    def __new__(mcs, *args: str, **kwargs: int) -> typing.Type[
        'PreviewBuilder']:
        cls = super().__new__(mcs, *args, **kwargs)
        cls = typing.cast(typing.Type['PreviewBuilder'], cls)
        cls.register()
        return cls


class PreviewBuilder(object, metaclass=PreviewBuilderMeta):
    mimetype = []  # type: typing.List[str]

    def __init__(
            self,
    ) -> None:
        logging.info('New Preview builder of class' + str(self.__class__))

    @classmethod
    def get_mimetypes_supported(
            cls,
    ) -> typing.List[str]:
        return cls.mimetype

    def get_page_number(self, file_path: str, preview_name: str,
                        cache_path: str) -> int:
        '''
        Get the number of page of the document
        '''
        raise Exception(
            'Number of pages not supported for this kind of Preview'
            ' Builder. Your preview builder must implement a '
            'get_page_number method with the same signature as in'
            'PreviewBuilder'
        )

    def build_jpeg_preview(self, file_path: str, preview_name: str,
                           cache_path: str, page_id: int,
                           extension: str = '.jpg',
                           size: typing.Tuple[int, int] = (256, 256)) -> None:
        """
        generate the jpg preview
        """
        raise Exception("Not implemented for this kind of document")

    def build_pdf_preview(self, file_path: str, preview_name: str,
                          cache_path: str, extension: str = '.pdf') -> None:
        """
        generate the jpeg preview
        """
        raise Exception("Not implemented for this kind of document")

    def build_html_preview(self, file_path: str, preview_name: str,
                           cache_path: str, extension: str = '.html') -> None:
        """
        generate the html preview
        """
        raise Exception("Not implemented for this kind of document")

    def build_json_preview(self, file_path: str, preview_name: str,
                           cache_path: str, page_id: int = 0,
                           extension: str = '.json') -> None:
        """
        generate the json preview
        """
        raise Exception("Not implemented for this kind of document")

    def build_text_preview(self, file_path: str, preview_name: str,
                           cache_path: str, page_id: int = 0,
                           extension: str = '.txt') -> None:
        """ 
        return file content from the cache
        """
        raise Exception("Not implemented for this kind of document")

    def get_jpeg_preview(self, file_path: str, preview_name: str,
                         cache_path: str, page_id: int,
                         extension: str = '.jpeg',
                         size: typing.Tuple[int, int] = (256, 256),
                         force: bool = False) -> str:

        if not self.exists_preview(
                        cache_path + preview_name, extension
        ) or force:
            self.build_jpeg_preview(
                file_path=file_path,
                preview_name=preview_name,
                cache_path=cache_path,
                page_id=page_id,
                extension=extension,
                size=size
            )

        if page_id == -1:
            return cache_path + preview_name + extension
        else:
            return '{cache}{file}{ext}'.format(
                cache=cache_path,
                file=preview_name,
                ext=extension,
            )

    def get_pdf_preview(self, file_path: str, preview_name: str,
                        cache_path: str, page: int = -1,
                        extension: str = '.pdf', force: bool = False) -> str:
        """ 
        return file content from the cache
        """
        if not self.exists_preview(
                path=cache_path + preview_name,
                extension=extension) or force:
            self.build_pdf_preview(
                file_path=file_path,
                preview_name=preview_name,
                cache_path=cache_path,
                extension=extension
            )

        if page == -1 or page == None:
            return cache_path + preview_name + extension
        else:
            with open(
                    '{path}{file_name}{extension}'.format(
                        path=cache_path,
                        file_name=preview_name,
                        extension=extension
                    ),
                    'rb'
            ) as handler:
                input_pdf = PdfFileReader(handler)
                output_pdf = PdfFileWriter()
                output_pdf.addPage(input_pdf.getPage(page))

                output_stream = BytesIO()
                output_pdf.write(output_stream)
                output_stream.seek(0, 0)

                with open('{path}{file_name}{extension}'.format(
                        path=cache_path,
                        file_name=preview_name,
                        page=page,
                        extension=extension
                ), 'wb') \
                        as paged_pdf:
                    output_stream.seek(0, 0)
                    buffer = output_stream.read(1024)
                    while buffer:
                        paged_pdf.write(buffer)
                        buffer = output_stream.read(1024)
            return '{path}{file_name}{extension}'.format(
                path=cache_path,
                file_name=preview_name,
                extension=extension
            )

    def get_html_preview(self, file_path: str, preview_name: str,
                         cache_path: str, extension: str = '.html',
                         force: bool = False) -> str:
        """ 
        return file content from the cache
        """
        if not self.exists_preview(cache_path + preview_name,
                                   extension=extension) or force:
            self.build_html_preview(
                file_path=file_path,
                preview_name=preview_name,
                cache_path=cache_path,
                extension=extension
            )
        return '{cache}{file}{ext}'.format(
            cache=cache_path,
            file=preview_name,
            ext=extension,
        )

    def get_json_preview(self, file_path: str, preview_name: str,
                         cache_path: str, extension: str = '.json',
                         force: bool = False) -> str:
        """ 
        return file content from the cache
        """
        if not self.exists_preview(path=cache_path + preview_name,
                                   extension=extension) or force:
            self.build_json_preview(
                file_path=file_path,
                preview_name=preview_name,
                cache_path=cache_path,
                extension=extension
            )
        return cache_path + preview_name + extension

    def get_text_preview(self, file_path: str, preview_name: str,
                         cache_path: str, extension: str = '.txt',
                         force: bool = False) -> str:
        """ 
        return file content from the cache
        """
        if not self.exists_preview(path=cache_path + preview_name,
                                   extension=extension) or force:
            self.build_text_preview(
                file_path=file_path,
                preview_name=preview_name,
                cache_path=cache_path,
                extension=extension
            )
        return '{cache}{file}{ext}'.format(
            cache=cache_path,
            file=preview_name,
            ext=extension,
        )

    def exists_preview(self, path: str,
                       extension: str = '') -> bool:
        """
        return true if the cache file exists
        """
        full_path = '{path}{extension}'.format(
            path=path,
            extension=extension
        )

        if os.path.exists(full_path):
            return True
        else:
            return False

    @classmethod
    def register(cls) -> None:
        PreviewBuilderFactory.get_instance().register_builder(cls)


class OnePagePreviewBuilder(PreviewBuilder):
    '''
    Generic preview handler for single page document
    '''

    def get_page_number(self, file_path: str, preview_name: str,
                        cache_path: str) -> int:
        return 1

    def exists_preview(self, path: str, page_id: int = None,
                       extension: str = '') -> bool:
        """
        return true if the cache file exists
        """
        full_path = '{path}{extension}'.format(
            path=path,
            extension=extension
        )
        if os.path.exists(full_path):
            return True
        else:
            return False

    def get_jpeg_preview(
            self, file_path: str, preview_name: str, cache_path: str,
            page_id: int, extension: str = '.jpeg',
            size: typing.Tuple[int, int] = (256, 256),
            force: bool = False) -> str:

        if (not self.exists_preview(cache_path + preview_name, page_id,
                                    extension)) or force:
            self.build_jpeg_preview(
                file_path=file_path,
                preview_name=preview_name,
                cache_path=cache_path,
                page_id=page_id,
                extension=extension,
                size=size
            )
        return cache_path + preview_name + extension


class ImagePreviewBuilder(OnePagePreviewBuilder):
    '''
    Generic preview handler for an Image (except multi-pages images)
    '''

    def build_json_preview(self, file_path: str, preview_name: str,
                           cache_path: str, page_id: int = 0,
                           extension: str = '.json') -> None:
        """
        generate the json preview
        """

        with open(file_path, 'rb') as img:
            result = file_converter.image_to_json(img)
            with open(cache_path + preview_name + extension, 'wb') as jpeg:
                buffer = result.read(1024)
                while buffer:
                    jpeg.write(buffer)
                    buffer = result.read(1024)
