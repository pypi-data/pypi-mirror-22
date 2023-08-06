# -*- coding: utf-8 -*-

"""
coq_install_coca.py is part of Coquery.

Copyright (c) 2016 Gero Kunter (gero.kunter@coquery.org)

Coquery is released under the terms of the GNU General Public License (v3).
For details, see the file LICENSE that you should have received along 
with Coquery. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import codecs
import csv
import itertools
import tempfile

from coquery.corpusbuilder import *
from coquery.defines import *
from coquery import options
from coquery.general import get_chunk

class BuilderClass(BaseCorpusBuilder):
    file_filter = "db_*_*.txt"

    corpus_table = "Corpus"
    corpus_id = "ID"
    corpus_word_id = "WordId"
    corpus_source_id = "SourceId"

    word_table = "Lexicon"
    word_id = "WordId"
    word_label = "Word"
    word_lemma = "Lemma"
    word_pos = "POS"

    source_table = "Sources"
    source_id = "SourceId"
    source_label = "Source"
    source_title = "Title"
    source_genre = "Genre"
    source_year = "Year"
    source_subgenre_id = "SubgenreId"
    
    subgenre_table = "Subgenres"
    subgenre_id = "SubgenreId"
    subgenre_label = "Subgenre"
    
    special_files = ["coca-sources.txt", "lexicon.txt", "Sub-genre codes.txt"]
    expected_files = special_files + [
        "db_acad_1990.txt", "db_acad_1991.txt", "db_acad_1992.txt", 
        "db_acad_1993.txt", "db_acad_1994.txt", "db_acad_1995.txt", 
        "db_acad_1996.txt", "db_acad_1997.txt", "db_acad_1998.txt", 
        "db_acad_1999.txt", "db_acad_2000.txt", "db_acad_2001.txt", 
        "db_acad_2002.txt", "db_acad_2003.txt", "db_acad_2004.txt", 
        "db_acad_2005.txt", "db_acad_2006.txt", "db_acad_2007.txt", 
        "db_acad_2008.txt", "db_acad_2009.txt", "db_acad_2010.txt", 
        "db_acad_2011.txt", "db_acad_2012.txt", "db_fic_1990.txt", 
        "db_fic_1991.txt", "db_fic_1992.txt", "db_fic_1993.txt", 
        "db_fic_1994.txt", "db_fic_1995.txt", "db_fic_1996.txt", 
        "db_fic_1997.txt", "db_fic_1998.txt", "db_fic_1999.txt", 
        "db_fic_2000.txt", "db_fic_2001.txt", "db_fic_2002.txt", 
        "db_fic_2003.txt", "db_fic_2004.txt", "db_fic_2005.txt", 
        "db_fic_2006.txt", "db_fic_2007.txt", "db_fic_2008.txt", 
        "db_fic_2009.txt", "db_fic_2010.txt", "db_fic_2011.txt", 
        "db_fic_2012.txt", "db_mag_1990.txt", "db_mag_1991.txt", 
        "db_mag_1992.txt", "db_mag_1993.txt", "db_mag_1994.txt", 
        "db_mag_1995.txt", "db_mag_1996.txt", "db_mag_1997.txt", 
        "db_mag_1998.txt", "db_mag_1999.txt", "db_mag_2000.txt", 
        "db_mag_2001.txt", "db_mag_2002.txt", "db_mag_2003.txt", 
        "db_mag_2004.txt", "db_mag_2005.txt", "db_mag_2006.txt", 
        "db_mag_2007.txt", "db_mag_2008.txt", "db_mag_2009.txt", 
        "db_mag_2010.txt", "db_mag_2011.txt", "db_mag_2012.txt", 
        "db_news_1990.txt", "db_news_1991.txt", "db_news_1992.txt", 
        "db_news_1993.txt", "db_news_1994.txt", "db_news_1995.txt", 
        "db_news_1996.txt", "db_news_1997.txt", "db_news_1998.txt", 
        "db_news_1999.txt", "db_news_2000.txt", "db_news_2001.txt", 
        "db_news_2002.txt", "db_news_2003.txt", "db_news_2004.txt", 
        "db_news_2005.txt", "db_news_2006.txt", "db_news_2007.txt", 
        "db_news_2008.txt", "db_news_2009.txt", "db_news_2010.txt", 
        "db_news_2011.txt", "db_news_2012.txt", "db_spok_1990.txt", 
        "db_spok_1991.txt", "db_spok_1992.txt", "db_spok_1993.txt", 
        "db_spok_1994.txt", "db_spok_1995.txt", "db_spok_1996.txt", 
        "db_spok_1997.txt", "db_spok_1998.txt", "db_spok_1999.txt", 
        "db_spok_2000.txt", "db_spok_2001.txt", "db_spok_2002.txt", 
        "db_spok_2003.txt", "db_spok_2004.txt", "db_spok_2005.txt", 
        "db_spok_2006.txt", "db_spok_2007.txt", "db_spok_2008.txt", 
        "db_spok_2009.txt", "db_spok_2010.txt", "db_spok_2011.txt", 
        "db_spok_2012.txt"]

    def __init__(self, gui=False, *args):
       # all corpus builders have to call the inherited __init__ function:
        super(BuilderClass, self).__init__(gui, *args)

        self.create_table_description(self.word_table,
            [Identifier(self.word_id, "MEDIUMINT(7) UNSIGNED NOT NULL"),
             Column(self.word_label, "VARCHAR(43) NOT NULL"),
             Column(self.word_lemma, "VARCHAR(24) NOT NULL"),
             Column(self.word_pos, "VARCHAR(24) NOT NULL")])

        self.create_table_description(self.subgenre_table,
            [Identifier(self.subgenre_id, "SMALLINT UNSIGNED"),
             Column(self.subgenre_label, "ENUM('ACAD:Education','ACAD:Geog/SocSci','ACAD:History','ACAD:Humanities','ACAD:Law/PolSci','ACAD:Medicine','ACAD:Misc','ACAD:Phil/Rel','ACAD:Sci/Tech','FIC:Gen (Book)','FIC:Gen (Jrnl)','FIC:Juvenile','FIC:Movies','FIC:SciFi/Fant','MAG:Afric-Amer','MAG:Children','MAG:Entertain','MAG:Financial','MAG:Home/Health','MAG:News/Opin','MAG:Religion','MAG:Sci/Tech','MAG:Soc/Arts','MAG:Sports','MAG:Women/Men','NEWS:Editorial','NEWS:Life','NEWS:Misc','NEWS:Money','NEWS:News_Intl','NEWS:News_Local','NEWS:News_Natl','NEWS:Sports','SPOK:ABC','SPOK:CBS','SPOK:CNN','SPOK:FOX','SPOK:Indep','SPOK:MSNBC','SPOK:NBC','SPOK:NPR','SPOK:PBS') NOT NULL")])

        self.create_table_description(self.source_table,
            [Identifier(self.source_id, "MEDIUMINT(7) UNSIGNED NOT NULL"),
             Column(self.source_year,  "SMALLINT(4) NOT NULL"),
             Column(self.source_genre, "CHAR(4) NOT NULL"),
             Link(self.source_subgenre_id, self.subgenre_table),
             Column(self.source_label, "VARCHAR(177)"),
             Column(self.source_title, "VARCHAR(499)")])

        self.create_table_description(self.corpus_table,
            [Identifier(self.corpus_id, "INT(9) UNSIGNED NOT NULL"),
             Link(self.corpus_word_id, self.word_table),
             Link(self.corpus_source_id, self.source_table)])

        self.add_time_feature(self.source_year)
    
    @staticmethod
    def get_name():
        return "COCA"

    @staticmethod
    def get_db_name():
        return "coca"
    
    @staticmethod
    def get_language():
        return "English"
    
    @staticmethod
    def get_language_code():
        return "en-US"
        
    @staticmethod
    def get_title():
        return "Corpus of Contemporary American English"
        
    @staticmethod
    def get_description():
        return [
            "The Corpus of Contemporary American English (COCA) is the largest freely-available corpus of English, and the only large and balanced corpus of American English. The corpus was created by Mark Davies of Brigham Young University, and it is used by tens of thousands of users every month (linguists, teachers, translators, and other researchers).",
            "The corpus contains more than 450 million words of text and is equally divided among spoken, fiction, popular magazines, newspapers, and academic texts. It includes 20 million words each year from 1990-2012 and the corpus is also updated regularly (the most recent texts are from Summer 2012). Because of its design, it is perhaps the only corpus of English that is suitable for looking at current, ongoing changes in the language."]

    @staticmethod
    def get_references():
        return ["Davies, Mark. (2008-) <i>The Corpus of Contemporary American English: 450 million words, 1990-present</i>. Available online at http://corpus.byu.edu/coca/"]

    @staticmethod
    def get_url():
        return "http://corpus.byu.edu/coca/"

    @staticmethod
    def get_license():
        return "COCA is available under the terms of a commercial license."

    @staticmethod
    def get_installation_note():
        _, _, db_type, _, _ = options.get_con_configuration()
        
        if db_type == SQL_MYSQL:
            return """
            <p><b>MySQL installation note</b><p>
            <p>The COCA installer uses a special feature of MySQL servers 
            which allows to load large chunks of data into the database in a 
            single step.</p>
            <p>This feature notably speeds up the installation of the COCA 
            corpus. However, it may be disabled on your MySQL servers. In that 
            case, the installation will fail with an error message similar to 
            the following: </p>
            <p><code>The used command is not allowed with this MySQL version</code></p>
            <p>Should the installation fail, please ask your MySQL server 
            administrator to enable loading of local in-files by setting the 
            option <code>local-infile</code> in the MySQL configuration file.
            </p>                
            """
        else:
            return None

    def build_load_files(self):

        files = sorted(self.get_file_list(self.arguments.path, self.file_filter))

        if self._widget:
            self._widget.progressSet.emit(len(files), "")

        for count, file_name in enumerate(files):
            if self._widget:
                self._widget.labelSet.emit("Reading '{}' (file %v out of %m)".format(os.path.basename(file_name)))
            logger.info("Reading {}".format(file_name))
                
            # There seems to be an issue when loading longer files into an
            # MySQL database. Sometimes, the connection is lost
            base_name = os.path.basename(file_name)
            encoding = "latin-1"
            if base_name == "coca-sources.txt":
                encoding = "cp850"
            else:
                encoding = "latin-1"

            with codecs.open(file_name, "r", encoding=encoding) as big_file:
                fillna = None
                if base_name in self.special_files:
                    if base_name == "lexicon.txt":
                        fillna = ""
                        table = self.word_table
                    elif base_name == "coca-sources.txt":
                        table = self.source_table
                    elif base_name == "Sub-genre codes.txt":
                        table = self.subgenre_table
                    else:
                        raise RuntimeError("Unexpected file name: {}".format(base_name))
                else:
                    table = self.corpus_table

                # Unfortunately, the connection to the MySQL server may break 
                # with larger files. It is as yet unclear whether this can be 
                # fixed on the server side by a suitable configuration. For 
                # the time being, we will break the text files into smaller 
                # chunks of currently 250000 lines. These chunks are written 
                # into temporary files, which are in turn read by the MySQL 
                # server using the LOAD DATA LOCAL INLINE command.
                # Sadly, this is not very fast.
                
                # Iterate the chunks:

                for i, lines in enumerate(get_chunk(big_file)):
                    if self.interrupted:
                        return
                    # create and fill temporary file:
                    temp_file = tempfile.NamedTemporaryFile("w", delete=False)
                    content = list(lines)
                    if base_name not in self.special_files:
                        self._corpus_id += len(content)
                        if i == 0:
                            skip = 1
                        else:
                            skip = None
                    
                    if sys.version_info < (3, 0):
                        temp_file.write(u"\n".join([x.strip() for x in content])
                                        .replace("\x00", "")
                                        .encode("utf-8"))
                    else:
                        s = "\n".join([x.strip() for x in content])
                        temp_file.write(s.replace("\x00", ""))
                    temp_file.close()

                    skip = None
                    if (base_name in self.special_files and base_name != "Sub-genre codes.txt" and i == 0):
                        skip = 1

                    kwargs = {
                        "header": skip,
                        "sep": "\t",
                        "quoting": 3,
                        "encoding": "cp850",
                        }

                    if base_name == "Sub-genre codes.txt":
                        kwargs["names"] = self.subgenre_id, self.subgenre_label
                    elif base_name == "lexicon.txt":
                        kwargs["names"] = self.word_id, self.word_label, self.word_lemma, self.word_pos
                        kwargs["error_bad_lines"] = False
                        kwargs["na_filter"] = False
                        kwargs["drop_duplicate"] = self.word_id
                    elif base_name == "coca-sources.txt":
                        kwargs["names"] = self.source_id, self.source_year, self.source_genre, self.source_subgenre_id, self.source_label, self.source_title
                    else:
                        kwargs["names"] = self.corpus_source_id, self.corpus_id, self.corpus_word_id

                    self.DB.load_infile(temp_file.name, 
                                        table, 
                                        fillna=fillna,
                                        **kwargs)

                    # load the temporary file containing a chunk from the big 
                    # file into the matching table name:
                    #self.DB.load_infile(temp_file.name, table, arguments)
                    os.remove(temp_file.name)
                    

            if self._widget:
                self._widget.progressUpdate.emit(count + 1)

if __name__ == "__main__":
    BuilderClass().build()
